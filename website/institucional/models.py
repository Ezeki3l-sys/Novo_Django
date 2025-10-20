from django.db import models

import datetime

# Create your models here.


class Slideshow(models.Model):
    imagem = models.ImageField(verbose_name ="Imagem", upload_to='slideshow/')
    titulo = models.CharField(verbose_name ="titulo",max_length=50, blank=True, null=True,)
    alt = models.CharField(verbose_name ="Alternative",max_length=100, blank=True, null=True,)
    descricao = models.TextField("Descrição",  blank=True, null= True)
    ativo = models.BooleanField("Imagem ativa?", default=True)

    class Meta:
        verbose_name_plural = 'SlideShow'
        verbose_name = 'SlideShow'
        ordering = ('titulo',)

    def __str__(self):
        return self.titulo