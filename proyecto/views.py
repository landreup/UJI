# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden,\
    HttpResponseNotFound

from forms import ProyectoAlumnoForm

from curso.controllers import cambiarCurso
from curso.queries import QueryCourse

from proyecto.controllers import gruposProyectosEnCursoTodos, gruposProyectosEnCursoProfesor, isEditable,\
    mensajeError
from usuario.queries import QueryUser
from proyecto.queries import QueryProject, QueryProjectUnresolvedInCourse

from curso.decorators import courseSelected
from usuario.eujierlogin import eujierlogin_coordinator, eujierlogin_teacher
from alumno.queries import QueryStudent
from datetime import datetime

@courseSelected
@eujierlogin_teacher
def listadoProyectosProfesor(request, user, course):
    titulo = "Projectes Assignats"
    enCurso = gruposProyectosEnCursoProfesor(course, user)
    finalizados = QueryProject().getListProjectByCourseStatusTutor(course, "F", user)
    anyadir = isEditable(course)
    editar = isEditable(course)
    vacio = not enCurso and not finalizados
    cursos = QueryCourse().getListCourse(request)
    fechaTope = course.fechaTope.strftime('%d/%m/%Y') if course.fechaTope else None
    return render_to_response('proyectoListado.html', locals())

@courseSelected
@eujierlogin_coordinator
def listadoProyectosCoordinador(request, user, course):
    titulo = "Gestió de Projectes"
    muestraTutor = True
    pendientes = QueryProject().getListProjectByCourseAndStatus(course, "P")
    enCurso = gruposProyectosEnCursoTodos(course)
    finalizados = QueryProject().getListProjectByCourseAndStatus(course, "F")
    anyadir = isEditable(course)
    editar = isEditable(course)
    vacio = not pendientes and not enCurso and not finalizados
    cursos = QueryCourse().getListCourse(request)
    fechaTope = course.fechaTope.strftime('%d/%m/%Y') if course.fechaTope else None
    return render_to_response('proyectoListado.html', locals())

@courseSelected
@eujierlogin_coordinator
def listadoProyectosCoordinadorProfesor(request, user, course, profesorid):
    user = QueryUser().getUserByUserUJI(profesorid)
    if not user:
        return HttpResponseNotFound()
    
    titulo = "Projectes que tutoritza " + user.nombre
    enCurso = gruposProyectosEnCursoProfesor(course, user)
    finalizados = QueryProject().getListProjectByCourseStatusTutor(course, "F", user)
    anyadir = isEditable(course)
    editar = isEditable(course)
    vacio = not enCurso and not finalizados
    cursos = QueryCourse().getListCourse(request)
    fechaTope = course.fechaTope.strftime('%d/%m/%Y') if course.fechaTope else None
    return render_to_response('proyectoListado.html', locals())
    
def cambiaCurso(request, curso):
    cambiarCurso(request, curso)
    return HttpResponseRedirect(request.path.split('curs/')[0])

@courseSelected
@eujierlogin_teacher    
def gestionProyectos(request, user, course, accion="nuevo", alumnoid="", profesorid=""):
    project = None
    errors = None
    tutor = None
    if not isEditable(course):
        return HttpResponseForbidden()
    
    coordinator = False
    if alumnoid :
        student = QueryStudent().getStudentByUserUJI(alumnoid)
        if student :
            project =  QueryProject().getProjectByCourseAndStudent(course, student)
            revision = QueryProjectUnresolvedInCourse().getProjectUnresolvedByProject(project)
            if revision : 
                errors= mensajeError(revision)
            if user == project.tutor :
                tutor = user if "professorat" in request.path else None
            else:
                if not user.isCoordinator():
                    return HttpResponseNotFound()
        else: 
            if accion != "nuevo" :
                return HttpResponseNotFound()

    if (request.method == "POST") :
        form = ProyectoAlumnoForm(request, accion, alumnoid, tutor)
        if (form.is_valid()):
            form.save()
            if tutor :
                ruta = '/professorat/projectes/'
            else:
                if profesorid :
                    ruta = '/coordinacio/projectes/' + profesorid + '/' 
                else:
                    ruta = '/coordinacio/projectes/'
            return HttpResponseRedirect(ruta)
    else: 
        form = ProyectoAlumnoForm(request, accion, alumnoid, tutor)
    
    ocultaCurso=True
    grupos = True
    
    return render_to_response('proyectoGestion.html', locals()) 
