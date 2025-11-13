from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home_area_restrita'),
    path('editar_perfil/<int:id>/', views.editar_perfil, name='editar_perfil'),
    path('meus-personagens/',views.meus_personagens, name='meus_personagens'),
    path('cadastrar-personagem/', views.cadastrar_personagem, name='cadastrar_personagem'),
    path('editar-personagem/<int:id>/', views.editar_personagem, name='editar_personagem'),
    path('detalhes-personagem/<int:id>/', views.detalhes_personagem, name='detalhes_personagem'),
    path('deletar-personagem/<int:id>/', views.deletar_personagem, name='deletar_personagem'),

    path('minhas-campanhas/',views.minhas_campanhas, name='minhas_campanhas'),
    path('cadastrar-campanha/', views.cadastrar_campanha, name='cadastrar_campanha'),
    path('excluir_campanha/<int:id>/', views.excluir_campanha, name='excluir_campanha'),
    path('editar_campanha/<int:id>/', views.editar_campanha, name='editar_campanha'),
    


    path('participar-campanha/<int:id>/', views.participar_campanha, name='participar_campanha'),
    path('mestre/detalhes_campanha/<int:id>/', views.detalhes_campanha, name='detalhes_campanha'),
    path('mestre/solicitacoes', views.solicitacoes, name='solicitacoes'), 
    path('jogar/mestre/salvar-anotacao/<int:id>/', views.salvar_anotacao_mestre, name='salvar_anotacao_mestre'),


    path('mestre/solicitacoes/aprovar/<int:id>/', views.decisao, name='aprovar'), 
    path('mestre/solicitacoes/reprovar/<int:id>/', views.decisao, name='reprovar'), 

    path('jogar/<int:id>/', views.jogar, name='jogar_campanha'),
    path('jogar/jogador/salvar-anotacao/<int:id>/', views.salvar_anotacao_jogador, name='salvar_anotacao_jogador'),

    path('jogar/jogador/salvar-vida/<int:id>/<int:vida>/', views.salvar_vida_jogador, name='salvar_vida_jogador'),
    path('jogador/solicitacoes/', views.solicitacoes_jogador, name='solicitacoes_jogador'),
 

]

