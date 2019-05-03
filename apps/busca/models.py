# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from ferramentas import nomear_imagem, nomear_sequencia
from django.db.models.signals import post_delete

import os

SEQ_TIPOS = (('P', u'Proteína'),
             ('N', u'Nucleotídeo'))


class Planta(models.Model):
    
    nome_popular = models.CharField(u'Nome Vulgar', max_length=200, blank=True, unique=True)
    nome_cientifico = models.CharField(u'Nome Científico', max_length=255)
    data = models.DateTimeField(auto_now_add=True, editable=False)
    descricao = models.TextField(u'Descrição')
    curiosidades = models.TextField(u'Outras Informações Relevantes', blank=True)
    referencias = models.TextField(u'Referências', blank=True)
    imagem = models.ImageField(upload_to=nomear_imagem, help_text='Máximo 100KB.',blank=True)
    autor = models.ForeignKey(User, blank=True, editable=False)
    
    class Meta:
		verbose_name = u'Organismo'
    
    def __unicode__(self):
        if self.nome_popular:
            return '%s (%s)' % (self.nome_cientifico, self.nome_popular)
        return '%s' % (self.nome_cientifico)        
    

class Sequencia(models.Model):
    
    titulo = models.CharField(u'Título', max_length=200)
    tipo = models.CharField(u'Tipo de Sequência',
                            max_length=1, choices=SEQ_TIPOS)    
    data = models.DateTimeField(auto_now_add=True, editable=False)
    planta = models.ForeignKey(Planta,verbose_name=u'Organismo')
    url = models.URLField(max_length=250, verify_exists=False,
                          help_text='Endereço de onde a sequência foi baixada (e.g. http://www.ncbi.nlm.nih.gov/nuccore/340806769).',
                          blank=True)
    arquivo = models.FileField(u'Sequência', upload_to=nomear_sequencia, help_text='Somente arquivos no formato FASTA.')
    autor = models.ForeignKey(User, blank=True, editable=False)
    
    def __unicode__(self):
        return self.titulo


# Signals

def remover_imagem(sender, instance, **kwargs):
    if os.path.exists(instance.imagem.path):
        os.remove(instance.imagem.path)

post_delete.connect(remover_imagem, sender=Planta)
