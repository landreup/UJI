from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('valoracion.views',
                url(r'^$', 'estadoValoracion'),
                url(r'^activa/$', 'activarValoracion'),
                url(r'^formulari/hite/(?P<hitoid>\d+)/crea/$', 'creaFormulario'),
                url(r'^formulari/evaluacio/(?P<evaluacionid>\d+)/reactivar/$', 'reActivarValoracion')
)