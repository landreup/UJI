from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

""" URLs de Tutoritzacio """
urlpatterns = patterns('',
              url(r'^professorat/projectes/', include('proyecto.urls.professorat')),
)

""" URLs de Coordinacio """
urlpatterns += (patterns('',
                url(r'^coordinacio/projectes/', include('proyecto.urls.coordinacio')),
                url(r'^coordinacio/professorat/', include('usuario.urls')),
                url(r'^coordinacio/cursos/', include('curso.urls')),
                url(r'^coordinacio/evaluacio/', include('evaluacion.urls')),
                url(r'^formulari/', include('valoracion.urls_formulario')),
                url(r'^aplicacio/', include('aplicacion.urls')),
))

""" URLs de Estudiants """
urlpatterns += (patterns('',
                url(r'valoracio/', 'valoracion.views.estadoValoracion')
))

""" URLs de Aplicació """
urlpatterns += (patterns('',
                url(r'', 'aplicacio.views.index')
))

urlpatterns += staticfiles_urlpatterns()