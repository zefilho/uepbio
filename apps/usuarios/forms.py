# coding: utf-8

from django import forms
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField

class RegistroUserForm(forms.Form):
    user = forms.CharField(label=u'Usuário', max_length=30)
    email = forms.EmailField(label=u'E-mail')
    senha = forms.CharField(widget=forms.PasswordInput)
    rsenha = forms.CharField(label=u'Repita a senha', widget=forms.PasswordInput)
    captcha = ReCaptchaField()
    

    def clean_user(self,  *args, **kwargs):
        user = self.cleaned_data.get('user')
        if user in ['login', 'logout', 'sucesso']:
            raise forms.ValidationError('Nome de usuário inválido! Tente outro nome.')
        elif User.objects.filter(username=user):
            raise forms.ValidationError('O nome de usuário já existe.')
        return user

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError('O e-mail já está cadastrado.')
        return email

    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('senha', '') != cleaned_data.get('rsenha', ''):
            raise forms.ValidationError('As senhas não são iguais!')
        return cleaned_data
