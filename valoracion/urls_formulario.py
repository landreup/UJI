from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('valoracion.views',
                url(r'^(?P<clave>.+)$', 'accesoFormularioPublico'),
)