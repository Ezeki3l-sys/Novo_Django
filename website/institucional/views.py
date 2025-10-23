from django.shortcuts import render, get_object_or_404, redirect
from website.institucional.models import Slideshow
from website.area_administrativa.models import Campanha, Usuario
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.contrib.auth.models import User
from django.db import IntegrityError


# Create your views here.
def home(request):
    slideshows = Slideshow.objects.filter(ativo=True)
    return render(request,'index.html',{'slideshows':slideshows})   

def explorar_campanhas(request):
    todas_campanhas = Campanha.objects.all().order_by('data_inicio', 'nome_campanha').exclude(mestre__username=request.user)

    if request.method == 'GET':
        return render(request, 'explorar_campanhas.html', {'campanhas': todas_campanhas, 'pesquisa': ''})

    pesquisar = request.POST.get('pesquisar_campanha', '').strip()
    
    if pesquisar:
        todas_campanhas = todas_campanhas.filter(
            Q(nome_campanha__icontains=pesquisar) | Q(mestre__first_name__icontains=pesquisar) | Q(mestre__username__icontains=pesquisar)
        )

    return render(request, 'explorar_campanhas.html', {'campanhas': todas_campanhas, 'pesquisa': pesquisar})

# def cadastro(request):
#     messages.add_message(request, constants.SUCCESS, 'Página carregada com sucesso')
#     return render(request,'cadastro.html') 


# def cadastro_adicionar(request):
#     if request.method == 'POST':
#         # Dados do formulário
#         primeiro_nome = request.POST.get('primeiroNome')
#         segundo_nome = request.POST.get('segundoNome')
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         senha = request.POST.get('senha')
#         senha2 = request.POST.get('senha2')
#         eh_mestre = request.POST.get('eh_mestre') is not None
#         eh_jogador = request.POST.get('eh_jogador') is not None
#         bio = request.POST.get('bio')
#         avatar = request.FILES.get('avatar')  # arquivos vêm de request.FILES
#         data_nascimento = request.POST.get('data')

#         # Validação simples
#         if senha != senha2:
#             messages.error(request, 'As senhas não coincidem.')
#             return render(request, 'cadastro.html')

#         try:
#             # Cria o User padrão
#             user = User.objects.create_user(
#                 username=username,
#                 password=senha,
#                 email=email,
#                 first_name=primeiro_nome,
#                 last_name=segundo_nome,
#             )

#             # Cria o perfil extendido (Usuario)
#             Usuario.objects.create(
#                 user=user,
#                 nome=f'{primeiro_nome} {segundo_nome}',
#                 nickname=username,
#                 email=email,
#                 data_nascimento=data_nascimento,
#                 bio=bio,
#                 avatar=avatar,
#                 eh_mestre=eh_mestre,
#                 eh_jogador=eh_jogador,
#             )

#             messages.success(request, 'Cadastro realizado com sucesso!')
#             return redirect('login')  # ou onde quiser

#         except IntegrityError:
#             messages.error(request, 'Esse nome de usuário ou email já existe.')
#             return render(request, 'cadastro.html')

#     return render(request, 'cadastro.html')

# def cadastro_adicionar2(request):
#     if request.method == 'POST':

#         primeiroNome_value = request.POST.get('primeiroNome')
#         segundooNome_value = request.POST.get('segundoNome')
#         username_value = request.POST.get('username')
#         email_value = request.POST.get('email')
#         senha_value = request.POST.get('senha')
#         senha2_value = request.POST.get('senha2')
#         eh_mestre_value = request.POST.get('eh_mestre')
#         eh_jogador_value = request.POST.get('eh_jogador')
#         bio_value = request.POST.get('bio')
#         avatar_value = request.POST.get('avatar')
#         data_nascimento_value = request.POST.get('data')
#         print(eh_mestre_value)
#         print(eh_jogador_value)
#         usuario_dados = {   
#                             'p_nome':primeiroNome_value,
#                             's_nome':segundooNome_value,
#                             'username':username_value,
#                             'email':email_value,
#                             'senha':senha_value,
#                             'mestre':  False if eh_mestre_value is None else True,
#                             'jogador': False if eh_jogador_value is None else True,
#                             'bio':bio_value,
#                             'avatar':avatar_value,
#                             'data':data_nascimento_value
#                         }         
#         print(usuario_dados)
#         print()
#         if (senha_value!=senha2_value):
#             messages.add_message(request, constants.ERROR, 'SEU BOSTA')
#             print(usuario_dados)
#             return render(request,'cadastro.html', {'usuario_dados':usuario_dados}) 



#         #REALIZAR O PROCEDIMENTO PARA SALVAR
      
#         #ANTES DE SALVAR VERIFICAR SE O USUARIO JA EXISTE
#         novo_usuario_instancia = Usuario.objects.filter(email=email_value).filter(nickname=username_value)
#         print(novo_usuario_instancia)

#         if (novo_usuario_instancia):
#             return HttpResponse(f"<h1>Já EXITE {primeiroNome_value} {segundooNome_value}!</h1> <script>alert('JA EXISTE')</script>")
        
        
#         #REALIZAR O PROCEDIMENTO PARA SALVAR
#         novo_usuario_instancia = Usuario(nome = f'{primeiroNome_value} {segundooNome_value}',
#                                         nickname = username_value,
#                                         email = email_value,
#                                         senha = senha_value,
#                                         eh_mestre = usuario_dados['mestre'],
#                                         eh_jogador = usuario_dados['jogador'],
#                                         bio = bio_value,
#                                         avatar = avatar_value,
#                                         data_nascimento = data_nascimento_value)
#         novo_usuario_instancia.save()
#         return redirect('login')
#         #return HttpResponse(f"<h1>Hello {primeiroNome_value} {segundooNome_value}!</h1> <script>alert('Usuário cadastrado com sucesso')</script>")

# def login_adicionar(request):
#     if request.method == 'POST':
    
#         email_value = request.POST.get('email')
#         senha_value = request.POST.get('senha')
#         print(senha_value,email_value)

#         novo_usuario_instancia = Usuario.objects.filter(email=email_value).filter(senha=senha_value)
#         if (novo_usuario_instancia):
#             return redirect('home')
#         else:
#             messages.add_message(request, constants.ERROR, 'SEU BOSTA, a senha e/ou email não conferem!')
#             return redirect('login')
            





# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)
#         print(user)
#         if user is not None:
#             login(request, user)  # cria sessão de usuário
#             return redirect('home')
#         else:
#             messages.error(request, 'Usuário ou senha inválidos.')

#     return render(request, 'login.html')


# @login_required(login_url='login')  # protege a view para usuários logados
# def home_view(request):
#     return render(request, 'home.html', {'user': request.user})


# def logout_view(request):
#     logout(request)  # destrói a sessão
#     return redirect('login')



# def lista_pessoas(request):
#     pessoas = Pessoa.objects.all().order_by('nome')
#     return render(request, 'pessoas.html', {'pessoas': pessoas})


# def pessoa_detalhe(request, id):
#     pessoa = get_object_or_404(Pessoa, id=id)
#     return render(request, 'pessoa_detalhe.html', {'pessoa': pessoa})