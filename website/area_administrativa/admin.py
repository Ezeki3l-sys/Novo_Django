from django.contrib import admin
from .models import Personagem, Classe, Campanha, PedidoParticipacaoCampanha

class PersonagemModelAdmin(admin.ModelAdmin):
    list_display = ['nome_personagem','avatar_personagem','raca','classe',]
    search_fields = ('nome_personagem',"raca", "classe")



admin.site.register(Personagem,PersonagemModelAdmin)

admin.site.register(Classe)

admin.site.register(Campanha)


admin.site.register(PedidoParticipacaoCampanha)
