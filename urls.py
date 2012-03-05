from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

""" URLs de Tutoritzacio """
urlpatterns = patterns('',
              url(r'^professorat/', include('evalua.urls_professorat')),
)

""" URLs de Coordinacio """
urlpatterns += (patterns('',
                url(r'^coordinacio/', include('evalua.urls_coordinacio')),
                url(r'^coordinacio/projectes/?', include('proyecto.urls.coordinacio')),
                url(r'^coordinacio/professorat/?', include('usuario.urls')),
                url(r'^coordinacio/cursos/?', include('curso.urls')),
))


urlpatterns += staticfiles_urlpatterns()