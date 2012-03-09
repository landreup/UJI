from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('proyecto.views',
        url(r'^$', 'listadoProyectos',  {'vista': ["coordinador"]}),
        url(r'^nou$', 'gestionProyectos'),
        url(r'^(?P<profesorid>\w+)$', 'listadoProyectos', {'vista': ["tutor", "coordinador"]})
        
)