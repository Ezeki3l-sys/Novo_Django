from django.urls import path
from . import views

#app_name = "institucional"

urlpatterns = [
    path('',views.home, name='home'),
    path('explorar-campanhas/',views.explorar_campanhas, name='explorar_campanhas'),
    # path('cadastro/',views.cadastro, name='cadastro'),
    #path('login/',views.login, name='login'),
    #path('login/entrar/',views.login_adicionar, name='login_adicionar'),

    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),

    # path('cadastro/add/',views.cadastro_adicionar, name='cadastro_adicionar'),
    # path('pessoas/', views.lista_pessoas, name='lista_pessoas'),
    # path('pessoas/<int:id>/', views.pessoa_detalhe, name='pessoa_detalhe'),
]

