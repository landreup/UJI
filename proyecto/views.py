# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden

from forms import ProyectoAlumnoForm

from controllers import tituloListadoProyectos, gruposProyectosEnCurso, listaProyectosPendientes, listaProyectosFinalizados
from curso.controllers import cambiarCurso
from curso.queries import QueryCourse

def listadoProyectos(request, vista, profesorid=""):
    titulo = tituloListadoProyectos(request, profesorid)
    muestraTutor = ("tutor" not in vista)
    pendientes = listaProyectosPendientes(request)
    enCurso = gruposProyectosEnCurso(request, profesorid)
    finalizados = listaProyectosFinalizados(request)
    grupos= True
    anyadir = QueryCourse().isActualCourseSelected(request)
    cursos = QueryCourse().getListCourse(request)
    return render_to_response('proyectoListado.html', locals())

def cambiaCurso(request, curso):
    cambiarCurso(request, curso)
    return HttpResponseRedirect(request.path.split('curs/')[0])
    
def gestionProyectos(request, accion="nuevo", alumnoid=""):
    if not QueryCourse().isActualCourseSelected(request):
        return HttpResponseForbidden()
    
    if (request.method == "POST") :
        form = ProyectoAlumnoForm(request, accion, alumnoid, "lee")
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/coordinacio/projectes/')
    else: 
        form = ProyectoAlumnoForm(request, accion, alumnoid)
    
    ocultaCurso=True
    grupos = True
    
    return render_to_response('proyectoGestion.html', locals()) 
