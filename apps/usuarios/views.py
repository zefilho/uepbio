from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Permission
from django.template import RequestContext
from forms import RegistroUserForm


def registro_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    form = RegistroUserForm(request.POST or None)
    if form.is_valid():
        user = User.objects.create_user(form.cleaned_data['user'],
                                form.cleaned_data['email'],
                                form.cleaned_data['senha'])
        user.is_staff = True
        perms = []
        perms.extend(Permission.objects.filter(codename__contains='planta'))
        perms.extend(Permission.objects.filter(codename__contains='sequencia'))
        user.user_permissions.add(*perms)
        user.save()
        return HttpResponseRedirect('/usuarios/registrar/sucesso/')
        
    return render_to_response('usuarios/registrar_final.html', {'form' : form},
                              context_instance=RequestContext(request))
                              
def usuario(request):
	return HttpResponseRedirect('/')


