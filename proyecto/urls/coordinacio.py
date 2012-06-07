from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('proyecto.views',
        url(r'^$', 'listadoProyectosCoordinador'),
        url(r'^nou$', 'gestionProyectos'),
        url(r'^(?P<profesorid>\w+)/?$', 'listadoProyectosCoordinadorProfesor'),
        url(r'^(?P<profesorid>\w+)/(?P<alumnoid>\w+)/edita/?$', 'gestionProyectos', {'accion': "edita"}),
        url(r'^(?P<alumnoid>\w+)/edita/?$', 'gestionProyectos', {'accion': "edita"}),
        url(r'^\w+/curso/(?P<curso>\d\d\d\d/\d\d\d\d)$', 'cambiaCurso'),
        url(r'^curs/(?P<curso>\d\d\d\d/\d\d\d\d)$', 'cambiaCurso'),
)

urlpatterns += patterns('',
                url(r'^(?P<alumnoid>\w+)/evaluacio/', include('valoracion.urls')), 
                url(r'^(?P<profesorid>\w+)/(?P<alumnoid>\w+)/evaluacio/', include('valoracion.urls')),
)