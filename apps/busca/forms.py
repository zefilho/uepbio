# coding: utf-8

from django import forms
from apps.busca.models import Planta, Sequencia


TIPOS = (('P', u'Organismo'),
         ('S', u'Sequência'))

class BlastForm(forms.Form):
	motif = forms.CharField(widget = forms.Textarea(), label = 'Blast')
    #filogenia = forms.FileField(label = 'Filogenia - Upload do alinhamento das sequências')
class AlinhamentoForm(forms.Form):
    sequencia_one = forms.CharField(label = u'Sequencia_Um',widget = forms.Textarea())
    sequencia_two = forms.CharField(label = u'Sequencia_Dois',widget = forms.Textarea())
    file_seq = forms.FileField(required=False)
    gap_extension = forms.CharField(label = u'Gap_Extension', initial = '0.2')
    gap_open = forms.CharField(label = u'Gap_Open_Penaly', initial = '10.0')
    gap_separation = forms.CharField(label = u'Gap_Separation_Distance', initial = '4')
    end_gap = forms.CharField(label = u'End_Gap', initial = '-1')


class BuscaForm(forms.Form):
    busca = forms.CharField()


class BuscaEscolhaForm(forms.Form):
    escolha = forms.ChoiceField(choices=TIPOS,widget=forms.Select(attrs={'class':'fancy'}))
    busca = forms.CharField(widget=forms.TextInput(attrs={'style':'width:450px;height:24px;'}))


class PlantaForm(forms.ModelForm):
    class Meta:
        model = Planta

    def clean_nome_cientifico(self):
        nome = self.cleaned_data['nome_cientifico']
        #if Planta.objects.filter(nome_cientifico=nome):
            #raise forms.ValidationError('O nome já existe no banco.')
        if len(nome.split()) < 2:
            raise forms.ValidationError('O nome deve seguir a nomenclatura binomial.')
        return nome
    
    #def clean_imagem(self):
        #img = self.cleaned_data['imagem']
        #if img._size > 104857:
         #   raise forms.ValidationError('Imagem muito grande! Insira uma imagem com, no máximo, 100KB.')
       # return img


class SequenciaForm(forms.ModelForm):
    class Meta:
        model = Sequencia

    def clean_titulo(self):
        titulo_ = self.cleaned_data['titulo']
        if Sequencia.objects.filter(titulo=titulo_):
            raise forms.ValidationError('O nome já existe no banco.')
        return titulo_

    def clean_arquivo(self):
        seq = self.cleaned_data['arquivo']
        extensao = seq.name.split('.')[-1]
        if extensao.lower() != 'fasta':
            raise forms.ValidationError('Insira um arquivo do tipo FASTA.')
        return seq
