from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('evaluacion.views',
        url(r'^$', 'listadoHitos'),
        url(r'^nou$', 'gestionEvaluaciones', {'campo': "hito"}),
        url(r'^hites/nou$', 'gestionEvaluaciones', {'campo': "hito"}),
        url(r'^hites/(?P<hito>\d+)/edita$', 'gestionEvaluaciones', {'accion': "editar", 'campo': "hito"}),
        url(r'^hites/(?P<hito>\d+)/evaluacions/nou$', 'gestionEvaluaciones', {'campo': "evaluacion"}),
        url(r'^hites/(?P<hito>\d+)/evaluacions/(?P<evaluacion>\d+)/edita$', 'gestionEvaluaciones', {'accion': "editar", 'campo': "evaluacion"}),
        url(r'^hites/(?P<hito>\d+)/evaluacions/(?P<evaluacion>\d+)/preguntes/nou$', 'gestionEvaluaciones', {'campo': "pregunta"}),
        url(r'^hites/(?P<hito>\d+)/evaluacions/(?P<evaluacion>\d+)/preguntes/(?P<pregunta>\d+)/edita$', 'gestionEvaluaciones', {'accion': "editar", 'campo': "pregunta"}),
        url(r'^curs/(?P<curso>\d\d\d\d/\d\d\d\d)$', 'cambiaCurso'),
        url(r'activa/', 'activaSistemaEvaluacion'),
#        url(r'^cambia/(?P<profesorid>\w+)/?', 'cambiaUsuario'),
        
)