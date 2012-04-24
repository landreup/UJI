# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden

from forms import ProyectoAlumnoForm

from controllers import listaProyectos, tituloListadoProyectos
from curso.controllers import listaCurso, cambiarCurso, esCursoActual

def listadoProyectos(request, vista, profesorid=""):
    titulo = tituloListadoProyectos(vista, profesorid)
    listado = listaProyectos(request, vista, profesorid)
    campo = "Projectes"
    muestraTutor = ("tutor" not in vista)
    
    anyadir = esCursoActual(request)
    cursos = listaCurso(request)
    return render_to_response('proyectoListado.html', locals())

def cambiaCurso(request, curso):
    cambiarCurso(request, curso)
    return HttpResponseRedirect(request.path.split('curs/')[0])
    
    
def gestionProyectos(request, accion="nuevo", alumnoid=""):
    if not esCursoActual(request):
        return HttpResponseForbidden()
    
    if (request.method == "POST") :
        form = ProyectoAlumnoForm(request, accion, alumnoid, "lee")
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/coordinacio/cursos')
    else: 
        form = ProyectoAlumnoForm(request, accion, alumnoid)
    
    ocultaCurso=True
    grupos = True
    
    return render_to_response('proyectoGestion.html', locals()) 
