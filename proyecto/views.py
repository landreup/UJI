from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from forms import ProyectoAlumnoForm

from controllers import listaProyectos, tituloListadoProyectos

def listadoProyectos(request, vista, profesorid=""):
    titulo = tituloListadoProyectos(vista, profesorid)
    listado = listaProyectos(request, vista, profesorid)
    campo = "Projectes"
    muestraTutor = ("tutor" not in vista)
    anyadir = True
    return render_to_response('proyectoListado.html', locals())

def gestionProyectos(request, accion="nuevo", alumnoid=""):
    if (request.method == "POST") :
        form = ProyectoAlumnoForm(request, accion, alumnoid, "lee")
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/coordinacio/cursos')
    else: 
        form = ProyectoAlumnoForm(request, accion, alumnoid)
    
    ocultaCurso=True
    grupos = True
    
    # CAMBIAR PLANTILLA PARA QUE RECIBA SOLO UN FORMULARIO
    return render_to_response('proyectoGestion.html', {
                                                   'accion': accion,
                                                   'alumnoid': alumnoid,
                                                   'form_alumno': form.alumnoForm, 
                                                   'form_proyecto': form.proyectoForm,
                                                   'ocultaCurso': ocultaCurso,
                                                   'grupos': grupos,
                                                   })
