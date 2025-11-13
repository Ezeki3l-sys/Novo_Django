from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Personagem, Classe, Campanha, Usuario, PedidoParticipacaoCampanha, CampanhaJogador
from datetime import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
# def home(request):
#     return HttpResponse(f"<h1>Hello</h1>")


@login_required
def home(request):
    meus_personagens = Personagem.objects.filter(usuario=request.user).order_by('nome_personagem')
    minhas_campanhas = Campanha.objects.filter(mestre=request.user).order_by('nome_campanha')
    quantidade_solicitacoes = PedidoParticipacaoCampanha.objects.filter(mestre=request.user).filter(status='P').count()
    quantidade_solicitacoes_jogador = PedidoParticipacaoCampanha.objects.filter(personagem__usuario=request.user).count()
    return render(request, "index-area-restrita.html", {'personagens': meus_personagens,'campanhas': minhas_campanhas,'quantidade_solicitacoes':quantidade_solicitacoes, 'quantidade_solicitacoes_jogador': quantidade_solicitacoes_jogador})

@login_required
def editar_perfil(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    print(usuario)
    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        if request.FILES.get('avatar'):
            usuario.avatar = request.FILES.get('avatar')
        usuario.bio = request.POST.get('bio')
        usuario.save()
        messages.success(request, f'Usuario {usuario.username} atualizado com sucesso!')
        return redirect('home_area_restrita')
    
    return render(request, 'editar_perfil.html', {'usuario_dados': usuario})


@login_required
def meus_personagens(request):
    meus_personagens = Personagem.objects.filter(usuario=request.user).order_by('nome_personagem')
    if request.method == 'GET':
        return render(request, 'personagens/index.html', {'personagens': meus_personagens,  'pesquisa': ''})

    meus_personagens = meus_personagens.filter(nome_personagem__icontains=request.POST.get('pesquisar_personagem'))    
    return render(request, 'personagens/index.html', {'personagens': meus_personagens, 'pesquisa': request.POST.get('pesquisar_personagem')})

@login_required
def cadastrar_personagem(request):
    if request.method == 'POST':
        nome = request.POST.get('nome_personagem')
        avatar = request.FILES.get('avatar_personagem')
        raca = request.POST.get('raca')
        var_classe = request.POST.get('classe')
        historia = request.POST.get('historia')

        instancia_classe =  Classe.objects.get(nome_classe=var_classe)

        personagem = Personagem.objects.create(
            usuario=request.user,
            nome_personagem=nome,
            avatar_personagem=avatar,
            raca=raca,
            classe=instancia_classe,
            historia=historia
        )
        messages.success(request, f'Personagem {personagem.nome_personagem} cadastrado com sucesso!')
        return redirect('meus_personagens')
    
    classes  = Classe.objects.all()
    return render(request, 'personagens/cadastrar.html', {'toda_classes':classes })

@login_required
def editar_personagem(request, id):
    personagem = get_object_or_404(Personagem, id=id)
    if request.method == 'POST':
        personagem.nome_personagem = request.POST.get('nome_personagem')
        if request.FILES.get('avatar_personagem'):
            personagem.avatar_personagem = request.FILES.get('avatar_personagem')
        personagem.raca = request.POST.get('raca')
        personagem.classe = request.POST.get('classe')
        personagem.historia = request.POST.get('historia')
        personagem.save()
        messages.success(request, f'Personagem {personagem.nome_personagem} atualizado com sucesso!')
        return redirect('meus_personagens')
    return render(request, 'personagens/editar.html', {'personagem': personagem})

@login_required
def detalhes_personagem(request, id):
    personagem = get_object_or_404(Personagem, id=id)
    return render(request, 'personagens/detalhes.html', {'personagem': personagem})

@login_required
def deletar_personagem(request, id):
    personagem = get_object_or_404(Personagem, id=id)
    if request.method == 'POST':
        personagem.delete()
        messages.success(request, f'Personagem {personagem.nome_personagem} deletado com sucesso!')
        return redirect('meus_personagens')
    return render(request, 'personagens/confirmar_exclusao.html', {'personagem': personagem})



@login_required
def minhas_campanhas(request):
    minhas_campanhas = Campanha.objects.filter(mestre=request.user).order_by('nome_campanha')
    '''
    PRECISA SEPARAR AS CAMPANHAS ONDE O USUARIO E MESTRE DAQUELE JOGO
    E AS CAMPANHAS ONDE ELE E JOGADOR
    '''
    minhas_campanhas_mestre = minhas_campanhas.filter(mestre=request.user).values()
    print(minhas_campanhas_mestre)
    minhas_campanhas_jogador =  CampanhaJogador.objects.filter(usuario=request.user)  #minhas_campanhas.exclude(mestre=request.user)

    return render(request, 'campanhas/index-campanhas.html', {'campanhas': minhas_campanhas, 'campanhas_mestre': minhas_campanhas_mestre, 'campanhas_jogador': minhas_campanhas_jogador})

@login_required
def detalhes_campanha(request, id):
    campanha = get_object_or_404(Campanha, id=id)

    # Só o mestre pode ver detalhes
    if campanha.mestre != request.user:
        return redirect('accounts:logout')  # ou uma página "sem permissão"    
    jogadores = CampanhaJogador.objects.filter(campanha=id)
    #print(jogadores)
    minhas_campanhas_mestre = (Campanha.objects.filter(id=id, mestre=request.user).order_by('nome_campanha').values())
    minhas_campanhas_json = json.dumps(list(minhas_campanhas_mestre), cls=DjangoJSONEncoder)
   
    #print(minhas_campanhas_mestre[0].get('anotacoes'))
    minhas_anotacoes =json.dumps(minhas_campanhas_mestre[0].get('anotacoes'), cls=DjangoJSONEncoder)
    return render(request, 'mestre/detalhes_campanha.html', {'campanha': campanha,'jogadores': jogadores, 'minhas_campanhas_json': minhas_campanhas_json, 'minhas_anotacoes': minhas_anotacoes})

@login_required
def salvar_anotacao_mestre(request, id):
    if request.method == 'POST':
        anotacao = json.loads(request.POST.get('anotacao_mestre'))  
        campanha_mestre = get_object_or_404(Campanha, id=id, mestre=request.user)
        print(anotacao)
        if (anotacao == ''):
            anotacao = {}
        campanha_mestre.anotacoes = anotacao
        campanha_mestre.save()

        return JsonResponse({
            "status": "ok",
            "redirect_url": reverse('detalhes_campanha', args=[campanha_mestre.id])
        })
    
    return JsonResponse({'status': 'erro', 'mensagem': 'Método inválido'}, status=400)

    
@login_required
def cadastrar_campanha(request):
    if request.method == 'POST':
        nome_campanha = request.POST.get('nome_campanha')
        if request.FILES.get('imagem_de_capa'):
            img_capa = request.FILES.get('imagem_de_capa')
        descricao = request.POST.get('descricao')
        dt_inicio = request.POST.get('data_inicio')
        dt_fim = request.POST.get('data_fim')
        
        campanha = Campanha.objects.create(
            mestre=request.user,
            nome_campanha=nome_campanha,
            imagem_de_capa=img_capa,
            descricao=descricao,
            data_inicio=dt_inicio,
            data_fim=dt_fim
        )
        messages.success(request, f'Campanha {campanha.nome_campanha} cadastrado com sucesso!')
        return redirect('minhas_campanhas')
    else:
        return render(request, 'campanhas/cadastrar-campanha.html')
    
@login_required
def excluir_campanha(request, id):
    campanha = get_object_or_404(Campanha, id=id)
    if request.method == 'POST':
        campanha.delete()
        messages.success(request, f'Campanha {campanha.nome_campanha} deletada com sucesso!')
        return redirect('minhas_campanhas')
    return render(request, 'campanhas/excluir_campanha.html', {'campanha': campanha})

@login_required
def editar_campanha(request, id):
    campanha = get_object_or_404(Campanha, id=id)
    if request.method == 'POST':
        campanha.nome_campanha = request.POST.get('nome_campanha')
        if request.FILES.get('imagem_de_capa'):
            campanha.imagem_de_capa = request.FILES.get('imagem_de_capa')
        campanha.data_inicio = request.POST.get('data_inicio')
        campanha.data_fim = request.POST.get('data_fim')
        campanha.descricao = request.POST.get('descricao')
        campanha.save()
        messages.success(request, f'Campanha {campanha.nome_campanha} atualizada com sucesso!')
        return redirect('minhas_campanhas')
    return render(request, 'campanhas/editar_campanha.html', {'campanha': campanha})



@login_required
def participar_campanha(request, id):
    campanha = get_object_or_404(Campanha, id=id)
    personagens = Personagem.objects.filter(usuario=request.user)
    print(personagens)
    #mestre = Usuario.objects.get(username=campanha.mestre)
    if request.method == 'POST':
        personagem_id = request.POST.get('personagem_selecionado')
        personagem_selecionado = None
        
        # Só tenta buscar o personagem se veio algo no POST
        if personagem_id:
            try:
                personagem_selecionado = personagens.get(id=personagem_id)
            except Personagem.DoesNotExist:
                personagem_selecionado = None  # Evita erro se o ID for inválid

        solicitacao = PedidoParticipacaoCampanha.objects.create(
            usuario_solicitante=request.user,
            personagem = personagem_selecionado,
            mestre = campanha.mestre,
            mensagem=request.POST.get('mensagem'),
            campanha = campanha
        )
        solicitacao.save()
        messages.success(request, f'Pedido da campanha {campanha.nome_campanha} enviado com sucesso!')
        return redirect('minhas_campanhas')
    return render(request, 'campanhas/participar_campanha.html', {'campanha': campanha,'personagens':personagens})


def solicitacoes(request):    
    solicitacoes = PedidoParticipacaoCampanha.objects.filter(mestre=request.user).filter(status="P")
    print(solicitacoes)
    return render(request, 'mestre/solicitacoes.html', {'solicitacoes':solicitacoes})


def decisao(request, id):
    if request.method == 'POST':
        d = request.POST.get('decisao')  # "A" (Aprovada) ou "R" (Reprovada)

        solicitacao = PedidoParticipacaoCampanha.objects.get(id=id)
        # ✅ segurança: só o mestre da campanha pode aprovar/reprovar
        if solicitacao.mestre != request.user:
            return redirect('solicitacoes')        
        solicitacao.status = d
        solicitacao.data_aprovacao = datetime.now()
        solicitacao.save()
        
        # ✅ Se foi aprovada, cria o registro em CampanhaJogador
        if d == "A":
            # Verifica se já existe (evita duplicações)
            existe = CampanhaJogador.objects.filter(
                campanha=solicitacao.campanha,
                personagem=solicitacao.personagem
            ).exists()

            if not existe:
                CampanhaJogador.objects.create(
                    campanha=solicitacao.campanha,
                    personagem=solicitacao.personagem,
                    usuario=solicitacao.usuario_solicitante,
                    vida_atual=solicitacao.personagem.vida,  # vida inicial do personagem
                    experiencia=0,
                    nivel=1,
                    status='ativo'
                )

    return redirect('solicitacoes')


@login_required
def jogar(request, id):
    campanha_jogadores = CampanhaJogador.objects.filter(campanha=id).first()
    jogador = get_object_or_404(CampanhaJogador, campanha=id, usuario=request.user)

    print(jogador)

    return render(request, 'campanhas/jogar/index-jogar.html', {'campanha_jogadores': campanha_jogadores, 'jogador': jogador})

@login_required
def salvar_anotacao_jogador(request, id):
    if request.method == 'POST':
        anotacao = request.POST.get('anotacao_jogador')
        campanha_jogador = get_object_or_404(CampanhaJogador, id=id, usuario=request.user)
        campanha_jogador.anotacoes = anotacao
        campanha_jogador.save()
        #return HttpResponse('Anotação salva com sucesso!')
        return redirect('jogar_campanha', id=campanha_jogador.campanha.id)
    
    return HttpResponse('Método inválido.', status=400)

# @login_required
# def salvar_vida_jogador(request, id, vida):
#     campanha = get_object_or_404(Campanha, pk=id)
#     jogador = get_object_or_404(CampanhaJogador, campanha=campanha, usuario=request.user)

#     jogador.vida_atual = vida
#     jogador.save()

#     return redirect('jogar_campanha', id=jogador.campanha.id)

@login_required
def salvar_vida_jogador(request, id, vida):
    campanha = get_object_or_404(Campanha, pk=id)
    jogador = get_object_or_404(CampanhaJogador, campanha=campanha, usuario=request.user)

    jogador.vida_atual = vida
    jogador.save()

    return JsonResponse({
        "status": "ok",
        "nova_vida": jogador.vida_atual,
        "redirect_url": reverse('jogar_campanha', args=[jogador.campanha.id])
    })

def mestres(request):
    return render(request, 'mestres/index.html')

def detalhes(request):
    return render(request, 'mestres/detalhesCampanha.html')

def sessoes(request):
    return render(request, 'mestres/sessoes .html')

def solicitacoes_jogador(request):
    solicitacoes = PedidoParticipacaoCampanha.objects.filter(usuario_solicitante=request.user)
    print(solicitacoes)

    return render(request, 'jogador/lista-solicitacao.html' , {'solicitacoes':solicitacoes})

def jogadores(request):
    return render(request, 'jogadores/index.html')