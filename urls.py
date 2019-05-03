from django.conf.urls.defaults import patterns, include
from django.conf import settings
from django.views.generic.simple import direct_to_template
from apps.busca.models import Planta, Sequencia
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('busca.views',

    (r'^$', 'index'),
    (r'^plantas/$', 'pagina_especifica', {'entidade': Planta,
                                          'tipo': 'P',
                                          'template': 'busca/plantas.html'}),
    (r'^plantas/(?P<planta_id>\d+)/$', 'perfil_planta'),
    (r'^plantas/busca/(?P<busca>\S+.*)/$', 'resultado_plantas'),
    (r'^sequencias/$', 'pagina_especifica', {'entidade': Sequencia,
                                             'tipo': 'S',
                                             'template': 'busca/sequencias.html'}),
    (r'^sequencias/(?P<planta_id>\d+)/$', 'pagina_sequencias'),
    (r'^sequencias/(?P<planta_id>\d+)/(?P<sequencia_id>\d+)/$', 'perfil_sequencia'),
    (r'^sequencias/busca/(?P<busca>.*)/$', 'resultado_sequencias'),
    (r'^alinhamento/', 'alinhamento'),
	(r'^blast/','motifs'),
)


urlpatterns += patterns('',
	(r'^usuarios/$', 'usuarios.views.usuario'),
    (r'^usuarios/registrar/$', 'usuarios.views.registro_user'),
    (r'^usuarios/registrar/sucesso/$', direct_to_template, {'template': 'usuarios/registro_sucesso.html'}),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'usuarios/login.html'}),
    (r'^usuarios/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)


urlpatterns += patterns('contato.views',
    (r'^contato/$', 'contato'),
)


urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^grappelli/', include('grappelli.urls')),
)

urlpatterns += staticfiles_urlpatterns()


if settings.DEBUG: # Problema com os downloads
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),)
