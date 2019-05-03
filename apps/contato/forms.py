from django import forms
from django.core.mail import send_mail
from captcha.fields import ReCaptchaField	

class ContatoForm(forms.Form):
    nome = forms.CharField(label='Nome')
    email = forms.EmailField(label='E-mail')
    assunto = forms.CharField(label='Assunto')
    mensagem = forms.CharField(label='Escreva sua mensagem', widget=forms.Textarea())
    captcha = ReCaptchaField()

    def enviar_email(self):
        itens = self.clean()
        titulo = '[uepbio] %s' % (itens['assunto'])
        conteudo = 'Nome: %s\nE-mail: %s\n\n%s' % (itens['nome'],
                                              itens['email'],
                                              itens['mensagem'])
        email = 'email@exemplo.com' # Coloque seu e-mail
        send_mail(titulo, conteudo, email, [email])
