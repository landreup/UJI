from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('proyecto.views',
        url(r'^$', 'listadoProyectosProfesor'),
        url(r'^nou$', 'gestionProyectos'),
        url(r'^curs/(?P<curso>\d\d\d\d/\d\d\d\d)$', 'cambiaCurso')
)

urlpatterns += patterns('',
                url(r'^(?P<alumnoid>\w+)/evaluacio/$', include('valoracion.urls')), 
)