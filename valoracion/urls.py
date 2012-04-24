from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('valoracion.views',
                url(r'^$', 'estadoValoracion'),
                url(r'^formulari/hite/(?P<hitoid>\d+)/crea/$', 'creaFormulario'),
)