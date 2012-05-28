# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden,\
    HttpResponseNotFound

from forms import ProyectoAlumnoForm

from curso.controllers import cambiarCurso
from curso.queries import QueryCourse
from usuario.eujierlogin import eujierlogin_coordinator, eujierlogin_teacher
from proyecto.controllers import gruposProyectosEnCursoTodos, gruposProyectosEnCursoProfesor
from usuario.queries import QueryUser
from proyecto.queries import QueryProject
from curso.decorators import courseSelected


@eujierlogin_teacher
def listadoProyectosProfesor(request, user):
    curso = QueryCourse().getCourseSelected(request)
    titulo = "Projectes Assignats"
    enCurso = gruposProyectosEnCursoProfesor(curso, user)
    finalizados = QueryProject().getListProjectByCourseStatusTutor(curso, "F", user)
    anyadir = QueryCourse().isActualCourseSelected(request)
    cursos = QueryCourse().getListCourse(request)
    return render_to_response('proyectoListado.html', locals())

@courseSelected
@eujierlogin_coordinator
def listadoProyectosCoordinador(request, user, course):
    curso = course
    
    titulo = "Gestió de Projectes"
    muestraTutor = True
    pendientes = QueryProject().getListProjectByCourseAndStatus(curso, "P")
    enCurso = gruposProyectosEnCursoTodos(curso)
    finalizados = QueryProject().getListProjectByCourseAndStatus(curso, "F")
    anyadir = QueryCourse().isActualCourseSelected(request)
    cursos = QueryCourse().getListCourse(request)
    return render_to_response('proyectoListado.html', locals())

@eujierlogin_coordinator
def listadoProyectosCoordinadorProfesor(request, user, profesorid):
    curso = QueryCourse().getCourseSelected(request)
    user = QueryUser().getUserByUserUJI(profesorid)
    if not user:
        return HttpResponseNotFound()
    
    titulo = "Projectes que tutoritza " + user.nombre
    enCurso = gruposProyectosEnCursoProfesor(curso, user)
    finalizados = QueryProject().getListProjectByCourseStatusTutor(curso, "F", user)
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
