# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from ferramentas import nomear_imagem


class Perfil(models.Model):
    instituicao = models.CharField(u'Instituição', max_length=150, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    apresentacao = models.TextField(u'Apresentação')
    interesses = models.CharField(max_length=250)
    imagem = models.ImageField(upload_to=nomear_imagem, blank=True)
    contatos = models.ManyToManyField('self', blank=True)
    user = models.ForeignKey(User, unique=True)

    def __unicode__(self):
        return self.user.username


# Signals
def remover_imagem(sender, instance, **kwargs):
    if os.path.exists(instance.imagem.path):
        os.remove(instance.imagem.path)

post_delete.connect(remover_imagem, sender=Perfil)