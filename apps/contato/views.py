# coding: utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from busca.forms import BuscaForm, BuscaEscolhaForm
from forms import ContatoForm

def contato(request):
    if request.method == 'POST':
        # Valida os campos do contato e envia um e-mail, caso estejam corretos.
        contato_form = ContatoForm(request.POST)
        if contato_form.is_valid():
            contato_form.enviar_email()
            # Exibe uma mensagem de sucesso.
            return HttpResponseRedirect('/contato/sucesso/')
    else:
        contato_form = ContatoForm()
    # Exibe a página de contato.
    busca_form = BuscaEscolhaForm()
    if request.GET:
        busca_form = BuscaEscolhaForm(request.GET)
        if busca_form.is_valid():
            escolha = busca_form.cleaned_data['escolha']
            busca = busca_form.cleaned_data['busca']
            
            if escolha == 'P':
                return HttpResponseRedirect('/plantas/busca/%s' % (busca,))
            elif escolha == 'S':
                return HttpResponseRedirect('/sequencias/busca/%s' % (busca,))
                
    return render_to_response('contato/contato_two.html', {'contato_form': contato_form,
															'busca_form':busca_form},
                              context_instance=RequestContext(request))


def sucesso(request):
    return render_to_response('contato/sucesso.html')
