from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home_area_restrita'),
    path('meus-personagens/',views.meus_personagens, name='meus_personagens'),
    path('cadastrar-personagem/', views.cadastrar_personagem, name='cadastrar_personagem'),
    path('editar-personagem/<int:id>/', views.editar_personagem, name='editar_personagem'),
    path('detalhes-personagem/<int:id>/', views.detalhes_personagem, name='detalhes_personagem'),
    path('deletar-personagem/<int:id>/', views.deletar_personagem, name='deletar_personagem'),

    path('minhas-campanhas/',views.minhas_campanhas, name='minhas_campanhas'),
    path('cadastrar-campanha/', views.cadastrar_campanha, name='cadastrar_campanha'),
    path('excluir_campanha/<int:id>/', views.excluir_campanha, name='excluir_campanha'),
    path('editar_campanha/<int:id>/', views.editar_campanha, name='editar_campanha'),
    path('detalhes_campanha/<int:id>/', views.detalhes_campanha, name='detalhes_campanha'),
]