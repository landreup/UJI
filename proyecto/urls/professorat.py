from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('proyecto.views',
        url(r'^$', 'listadoProyectos',  {'vista': ["tutor"]}),
        url(r'^nou$', 'gestionProyectos'),
        url(r'^(?P<profesorid>\w+)$', 'listadoProyectos', {'vista': ["tutor", "coordinador"]}),
        url(r'^curso/(?P<curso>\d\d\d\d/\d\d\d\d)$', 'cambiaCurso')
)