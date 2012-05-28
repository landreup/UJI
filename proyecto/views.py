# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden,\
    HttpResponseNotFound

from forms import ProyectoAlumnoForm

from curso.controllers import cambiarCurso
from curso.queries import QueryCourse
from usuario.eujierlogin import eujierlogin_coordinator, eujierlogin_teacher
from proyecto.controllers import gruposProyectosEnCursoTodos, gruposProyectosEnCursoProfesor, listaProyectosPendientes, listaProyectosFinalizados
from usuario.queries import QueryUser

@eujierlogin_teacher
def listadoProyectosProfesor(request, user=None):
    titulo = "Projectes Assignats"
    enCurso = gruposProyectosEnCursoProfesor(request, user)
    # Finalizados
    anyadir = QueryCourse().isActualCourseSelected(request)
    cursos = QueryCourse().getListCourse(request)
    return render_to_response('proyectoListado.html', locals())

@eujierlogin_coordinator
def listadoProyectosCoordinador(request):
    titulo = "Gestió de Projectes"
    muestraTutor = True
    pendientes = listaProyectosPendientes(request)
    enCurso = gruposProyectosEnCursoTodos(request)
    finalizados = listaProyectosFinalizados(request)
    anyadir = QueryCourse().isActualCourseSelected(request)
    cursos = QueryCourse().getListCourse(request)
    return render_to_response('proyectoListado.html', locals())

@eujierlogin_coordinator
def listadoProyectosCoordinadorProfesor(request, profesorid):
    user = QueryUser().getUserByUserUJI(profesorid)
    if not user:
        return HttpResponseNotFound()
    
    titulo = "Projectes que tutoritza " + user.nombre
    enCurso = gruposProyectosEnCursoProfesor(request, user)
    # Finalizados
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
