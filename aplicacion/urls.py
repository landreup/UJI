from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('aplicacion.views',
        url(r'^inicia/$', 'iniciaAplicacion'),
)