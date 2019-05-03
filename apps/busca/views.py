# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.db.models import Q
from models import Planta, Sequencia
from forms import BuscaForm, BuscaEscolhaForm, AlinhamentoForm, BlastForm
from ferramentas import paginar,alinhar,motifs_teste
from django.conf import settings


def index(request):
    '''Página inicial do site.'''
    if request.GET:
        busca_form = BuscaEscolhaForm(request.GET)
        if busca_form.is_valid():
            escolha = busca_form.cleaned_data['escolha']
            busca = busca_form.cleaned_data['busca']
            
            if escolha == 'P':
                return HttpResponseRedirect('/plantas/busca/%s' % (busca,))
            elif escolha == 'S':
                return HttpResponseRedirect('/sequencias/busca/%s' % (busca,))      
    busca_form = BuscaEscolhaForm()     
    return render_to_response('test.html', {'busca_form': busca_form},
                              context_instance=RequestContext(request))


def pagina_especifica(request, tipo, entidade, template):
    '''Pagina genérica que exibe tanto a página principal das plantas quanto das sequências.'''
    if request.GET:
        busca_form = BuscaEscolhaForm(request.GET)
        if busca_form.is_valid():
            escolha = busca_form.cleaned_data['escolha']
            busca = busca_form.cleaned_data['busca']
            if escolha == 'P':
                return HttpResponseRedirect('/plantas/busca/%s' % (busca,))
            elif escolha == 'S':
                return HttpResponseRedirect('/sequencias/busca/%s' % (busca,))      
    busca_form = BuscaEscolhaForm(initial={'escolha': tipo})     
    ultimas = entidade.objects.all().order_by('-data')[:10]
    return render_to_response(template, {'ultimas': ultimas,
                                         'busca_form': busca_form},
                              context_instance=RequestContext(request))


def perfil_planta(request, planta_id):
    '''Página que exibe o perfil de uma planta, com sua foto e últimas sequências relacionadas.'''
    planta = Planta.objects.get(pk=planta_id)
    sequencias = planta.sequencia_set.all().order_by('-data')[:5]
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
    return render_to_response('busca/perfil_planta2.html', {'planta': planta,
															'busca_form':busca_form,
                                                           'sequencias': sequencias},
                              context_instance=RequestContext(request))


def perfil_sequencia(request,planta_id, sequencia_id):
    '''Página que exibe o perfil de uma sequência, com informações sobre data, titulo, opção para download e a sequência.'''
    planta = Planta.objects.get(pk=planta_id)
    sequencia = planta.sequencia_set.get(pk=sequencia_id)
    conteudo_seq = ''.join(sequencia.arquivo.readlines())
    if request.GET:
        busca_form = BuscaEscolhaForm(request.GET)
        if busca_form.is_valid():
            escolha = busca_form.cleaned_data['escolha']
            busca = busca_form.cleaned_data['busca']
            
            if escolha == 'P':
                return HttpResponseRedirect('/plantas/busca/%s' % (busca,))
            elif escolha == 'S':
                return HttpResponseRedirect('/sequencias/busca/%s' % (busca,))      
    busca_form = BuscaEscolhaForm() 
    return render_to_response('busca/perfil_seq.html', {'planta': planta,
                                                              'sequencia': sequencia,
                                                              'conteudo_seq': conteudo_seq,
                                                              'busca_form':busca_form},
                              context_instance=RequestContext(request))


def resultado_plantas(request, busca):
    '''Página que exibe o resultado de uma busca para plantas.'''
    if request.GET:
        busca_form = BuscaEscolhaForm(request.GET)
        if busca_form.is_valid():
            escolha = busca_form.cleaned_data['escolha']
            busca = busca_form.cleaned_data['busca']
            if escolha == 'P':
                return HttpResponseRedirect('/plantas/busca/%s' % (busca,))
            elif escolha == 'S':
                return HttpResponseRedirect('/sequencias/busca/%s' % (busca,))      
    # Filtrando a busca
    query = Q(nome_popular__icontains=busca) | \
            Q(nome_cientifico__icontains=busca)
    lista_resultado = Planta.objects.filter(query)
    tamanho = len(lista_resultado)
    resultado = paginar(lista_resultado, request)
    busca_form = BuscaEscolhaForm(initial={'busca': request.GET.get('busca', busca)})
    return render_to_response('busca/resul_planta.html', {'resultado': resultado,
                                                               'busca': busca,
                                                               'busca_form': busca_form,
                                                               'range': range(1,resultado.paginator.num_pages+1),
                                                               'tamanho':tamanho},
                               context_instance=RequestContext(request))


def resultado_sequencias(request, busca):
    '''Página que exibe o resultado de uma busca para sequências.'''
    if request.GET:
        busca_form = BuscaEscolhaForm(request.GET)
        if busca_form.is_valid():
            escolha = busca_form.cleaned_data['escolha']
            busca = busca_form.cleaned_data['busca']
            if escolha == 'P':
                return HttpResponseRedirect('/plantas/busca/%s' % (busca,))
            elif escolha == 'S':
                return HttpResponseRedirect('/sequencias/busca/%s' % (busca,))      
    # Filtrando a busca
    lista_resultado = Sequencia.objects.filter(titulo__icontains=busca)
    tamanho = len(lista_resultado)
    resultado = paginar(lista_resultado, request)
    busca_form = BuscaEscolhaForm(initial={'escolha': 'S', 'busca': request.GET.get('busca', busca)})
    return render_to_response('busca/resul_seq.html', {'resultado': resultado,
                                                                  'busca': busca,
                                                                  'busca_form': busca_form,
                                                                  'range': range(1,resultado.paginator.num_pages+1),
                                                                  'tamanho':tamanho},
                               context_instance=RequestContext(request))


def pagina_sequencias(request, planta_id):
    '''Página que exibe o resultado de uma busca para sequências de acordo com uma planta selecionada.'''
    planta = Planta.objects.get(pk=planta_id)
    lista_sequencias = planta.sequencia_set.all()
    sequencias = paginar(lista_sequencias, request)
    return render_to_response('busca/pagina_sequencias.html', {'planta': planta,
                                                               'sequencias': sequencias})
															   
#views que receber as requisoes e realiza o alinhamento															   
def alinhamento(request):
    busca_form = BuscaEscolhaForm(request.GET or None)
    if busca_form.is_valid():
        escolha = busca_form.cleaned_data['escolha']
        busca = busca_form.cleaned_data['busca']
            
        if escolha == 'P':
            return HttpResponseRedirect('/plantas/busca/%s' % (busca,))
        elif escolha == 'S':
            return HttpResponseRedirect('/sequencias/busca/%s' % (busca,)) 


    alinhamento = AlinhamentoForm(request.POST or None)
    if alinhamento.is_valid():
        seq_one = alinhamento.cleaned_data['sequencia_one']
        seq_two = alinhamento.cleaned_data['sequencia_two']

        result_one, result_two, fasta = alinhar(seq_one, seq_two)
		
		#return HttpResponse('%s' %fasta)
        return render_to_response('alinhamento/alinhamento_result.html', {'busca_form':busca_form,'teste':result_one,'teste2':result_two,'fasta':'%s'%(fasta),'path':settings.PROJECT_PATH},context_instance=RequestContext(request))
		
    return render_to_response('alinhamento/alinhamento.html',{'form':alinhamento, 'busca_form':busca_form},context_instance=RequestContext(request))                                                              
                                                               
#realizando motifs

def motifs(request):
    busca_form = BuscaEscolhaForm(request.GET or None)
    if busca_form.is_valid():
        escolha = busca_form.cleaned_data['escolha']
        busca = busca_form.cleaned_data['busca']
            
        if escolha == 'P':
            return HttpResponseRedirect('/plantas/busca/%s' % (busca,))
        elif escolha == 'S':
            return HttpResponseRedirect('/sequencias/busca/%s' % (busca,))
    
    motif_seq = BlastForm(request.POST or None)
    if motif_seq.is_valid():
        motif = motif_seq.cleaned_data['motif']
		#return HttpResponse(motifs_teste('seq'))
        return render_to_response('alinhamento/blast_result.html',{'busca_form':busca_form,'blast':'%s'%motifs_teste('seq')},context_instance = RequestContext(request))
		
    return render_to_response('alinhamento/blast.html',{'motifs':motif_seq,'busca_form':busca_form},context_instance = RequestContext(request))