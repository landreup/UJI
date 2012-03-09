from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('usuario.views',
        url(r'^$', 'listadoProfesores'),
        url(r'^nou$', 'gestionProfesor'),
        url(r'^(?P<profesorid>\w+)/edita$', 'gestionProfesor', {'accion': "editar"}),
        
)