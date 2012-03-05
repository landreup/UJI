from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('curso.views',
        url(r'$', 'listadoCursos'),
        url(r'/nou$', 'nuevoCurso'),
        url(r'/nou/confirmat/?$', 'nuevoCurso', {'confirma': True}),
)