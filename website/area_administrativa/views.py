from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Personagem, Classe, Campanha, Usuario, PedidoParticipacaoCampanha
from datetime import datetime
# Create your views here.
# def home(request):
#     return HttpResponse(f"<h1>Hello</h1>")


@login_required
def home(request):
    meus_personagens = Personagem.objects.filter(usuario=request.user).order_by('nome_personagem')
    minhas_campanhas = Campanha.objects.filter(mestre=request.user).order_by('nome_campanha')
    return render(request, "index-area-restrita.html", {'personagens': meus_personagens,'campanhas': minhas_campanhas})

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
    return render(request, 'campanhas/index-campanhas.html', {'campanhas': minhas_campanhas})

@login_required
def detalhes_campanha(request, id):
    jogadores = PedidoParticipacaoCampanha.objects.filter(mestre=request.user).filter(status="A")
    campanha = get_object_or_404(Campanha, id=id)
    return render(request, 'campanhas/detalhes_campanha.html', {'campanha': campanha,'jogadores': jogadores})

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
        d = request.POST.get('decisao')  

        solicitacao = PedidoParticipacaoCampanha.objects.get(id=id)
        solicitacao.status = d
        solicitacao.data_aprovacao = datetime.now()
        solicitacao.save()

    return redirect('solicitacoes')


def mestres(request):
    return render(request, 'mestres/index.html')

def detalhes(request):
    return render(request, 'mestres/detalhesCampanha.html')

def sessoes(request):
    return render(request, 'mestres/sessoes .html')


def jogadores(request):
    return render(request, 'jogadores/index.html')