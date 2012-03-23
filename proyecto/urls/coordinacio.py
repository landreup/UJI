from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('proyecto.views',
        url(r'^$', 'listadoProyectos',  {'vista': ["coordinador"]}),
        url(r'^nou$', 'gestionProyectos'),
        url(r'^(?P<profesorid>\w+)/?$', 'listadoProyectos', {'vista': ["tutor", "coordinador"]}),
        url(r'^(?P<alumnoid>\w+)/edita/?$', 'gestionProyectos', {'accion': "edita"}),
        url(r'^\w+/curso/(?P<curso>\d\d\d\d/\d\d\d\d)$', 'cambiaCurso'),
        url(r'^curso/(?P<curso>\d\d\d\d/\d\d\d\d)$', 'cambiaCurso')
)