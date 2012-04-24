from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('proyecto.views',
        url(r'^$', 'listadoProyectos',  {'vista': ["tutor"]}),
        url(r'^nou$', 'gestionProyectos'),
        url(r'^(?P<profesorid>\w+)$', 'listadoProyectos', {'vista': ["tutor", "coordinador"]}),
        url(r'^curs/(?P<curso>\d\d\d\d/\d\d\d\d)$', 'cambiaCurso')
)

urlpatterns += patterns('',
                url(r'^(?P<alumnoid>\w+)/evaluacio/$', include('valoracion.urls')), 
)