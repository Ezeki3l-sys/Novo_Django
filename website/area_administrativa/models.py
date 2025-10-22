from django.db import models
from website.usuarios.models import Usuario
 
# Create your models here.
class Classe(models.Model):
    nome_classe = models.CharField(verbose_name ="classe",max_length=100, blank=True, null=True,)

    class Meta:
        verbose_name_plural = 'Classes'
        verbose_name = 'Classe'
        ordering = ('nome_classe',)

    def __str__(self):
        return self.nome_classe

class Personagem(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank = True, null = True)
    nome_personagem = models.CharField(verbose_name ="personagem",max_length=50, blank=False, null=False,)
    avatar_personagem = models.ImageField(verbose_name ="avatar", upload_to='personagens/')
    raca = models.CharField(verbose_name ="raça",max_length=50, blank=True, null=True,)
    classe = models.ForeignKey(Classe, on_delete=models.DO_NOTHING, blank = True, null = True, related_name="personagens" )
    #classe = models.CharField(verbose_name ="classe",max_length=100, blank=True, null=True,)
    historia = models.TextField(verbose_name ="historia",  blank=True, null= True)

    class Meta:
        verbose_name_plural = 'Personagens'
        verbose_name = 'Personagem'
        ordering = ('nome_personagem',)

    def __str__(self):
        return self.nome_personagem
    
class Campanha(models.Model):
        mestre = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank = True, null = True)
        nome_campanha = models.CharField(verbose_name ="campanha",max_length=50, blank=False, null=False,)
        imagem_de_capa = models.ImageField(verbose_name ="imagem", upload_to='campanhas/')
        descricao = models.TextField(verbose_name ="descricao",max_length=50, blank=True, null=True,)
        data_inicio = models.DateField(blank = False, null = False )
        data_fim = models.DateField(blank=True, null= True)

        class Meta:
             verbose_name_plural = 'Campanhas'
             verbose_name = 'Campanha'
             ordering = ('nome_campanha',)

        def __str__(self):
             return self.nome_campanha
class PedidoParticipacaoCampanha(models.Model):
    PENDENTE = "P"
    APROVADA = "A"
    REPROVADA = "R"

    SITUACAO_CHOICES = (
        (PENDENTE, 'Pendente'),
        (APROVADA, 'Aprovada'),
        (REPROVADA, 'Reprovada'),
    )        

    usuario_solicitante = models.ForeignKey(
        Usuario,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='pedidos_solicitados'
    )
    mestre = models.ForeignKey(
        Usuario,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='pedidos_como_mestre'
    )
    campanha = models.ForeignKey(
        Campanha,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    mensagem = models.TextField(verbose_name="mensagem", max_length=100, blank=True, null=True)
    data_solicitacao = models.DateField(auto_now_add=True)
    data_aprovacao = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=SITUACAO_CHOICES, default=PENDENTE)

    class Meta:
        verbose_name = 'Pedido de participação da campanha'
        verbose_name_plural = 'Pedidos de participação da campanha'
        ordering = ('-data_solicitacao',)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario_solicitante}"
