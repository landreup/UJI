from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from forms import ProyectoAlumnoForm

from evalua.controllers.titulos import tituloListadoProyectos
from controllers import listaProyectos

def listadoProyectos(request, vista, profesorid=""):
    titulo = tituloListadoProyectos(vista, profesorid)
    listadoProyectos = listaProyectos(request, vista, profesorid)
    
    return render_to_response('alumnoListado.html', {'listaProyectos': listadoProyectos, 'rol': vista, 'titulo': titulo})

def gestionProyectos(request, accion="nuevo", alumnoid=""):
    if (request.method == "POST") :
        form = ProyectoAlumnoForm(request, accion, alumnoid, "lee")
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/coordinacio/cursos')
    else: 
        form = ProyectoAlumnoForm(request, accion, alumnoid)
    
    # CAMBIAR PLANTILLA PARA QUE RECIBA SOLO UN FORMULARIO
    return render_to_response('alumnoGestion.html', {
                                                   'accion': accion,
                                                   'alumnoid': alumnoid,
                                                   'form_alumno': form.alumnoForm, 
                                                   'form_proyecto': form.proyectoForm,
                                                   })
