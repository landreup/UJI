# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden

from forms import EvaluationFormForm
from queries import QueryEvaluationSystemTreeCompleteOfProject, QueryForm

from alumno.controllers import alumnoPorId
from curso.queries import QueryCourse
from proyecto.queries import QueryProject
from evaluacion.queries import QueryEvaluationSystem, QueryItem, QueryEvaluation
from valoracion.controllers import activaFormulario, activaValoracion

from usuario.eujierlogin import eujierlogin, loginFromEujierlogin,\
    eujierlogin_coordinator
from usuario.queries import QueryUser
from curso.decorators import courseSelected
from alumno.queries import QueryStudent

@courseSelected
@eujierlogin
def estadoValoracion(request, login, course, alumnoid):    
    evaluationSystem = QueryEvaluationSystem().getEvaluationSystemByCourse(course)
    if not evaluationSystem:
        return HttpResponseNotFound()
    
    if not evaluationSystem.isActive():
        return HttpResponseNotFound()
    
    student = QueryStudent().getStudentByUserUJI(alumnoid)
    if not student : return HttpResponseNotFound()

    project = QueryProject().getProjectByCourseAndStudent(course, student)
    if not (project): return HttpResponseNotFound()
    coordinator = False
    if login == alumnoid :
        rol = "A"
    else:
        if login in QueryProject().getloginByRol(project, "TU") and "professorat" in request.path:
            rol = "TU"
            user = QueryUser().getUserByUserUJI(login)
            if not user : return HttpResponseForbidden()
        else:
            coordinator = QueryUser().getUserCoordinatorByUserUJI(login)
            if not coordinator : return HttpResponseForbidden()     
            user = coordinator
            rol = "C"
            
    
    hitos = QueryEvaluationSystemTreeCompleteOfProject(project, True, rol).getList()
    
    grupos = True
    activar=project.isUnresolved()
    cursoActual = QueryCourse().getLastCourse() == course
    return render_to_response("sistemaEvaluacionValoradoListado.html", locals())

def creaFormulario(request, user, alumnoid, hitoid):
    # COMPROBAR ACCESO
    ''' Coordinador o tutor y proyecto en estado "P" y anteriores hitos completados '''
    course = QueryCourse().getCourseSelected(request)
    student = alumnoPorId(alumnoid)
    project = QueryProject().getProjectByCourseAndStudent(course, student)
    
    item = QueryItem().getItemByItem(hitoid)
    if not project : return HttpResponseNotFound()
    if project.estado != "P": return HttpResponseForbidden()
    if not item: return HttpResponseNotFound()
    
    ''' Anteriores hitos completados '''
    itemBefore = QueryItem().getBeforeItem(item)

    if itemBefore :
        response = QueryForm().isAllFormsCompletedOfProjectItem(project, itemBefore) 
        if not response:
            return HttpResponseForbidden()
        
    if (request.method == "POST"):
        activaFormulario(project, item)
        return HttpResponseRedirect('/coordinacio/projectes/')
        
    return render_to_response('creaFormulario.html', locals())

def accesoFormularioPublico(request, clave):
    formForm = QueryForm().getFormByKey(clave)
    if not formForm: return HttpResponseNotFound()
    access = True
    user = None
    if formForm.needUJIAuthentication() :
        access = False
        login, redirect = loginFromEujierlogin(request)
        if not login:
            return redirect
        if QueryProject().isUserRolinProject(formForm.proyecto, formForm.rol, login):
            access = True
            user = QueryUser().getUserByUserUJI(login)
        else:
            coordinador = QueryUser().getUserCoordinatorByUserUJI(login)
            user = coordinador
            if coordinador: access = True
            
    if access :
        return formularioPublico(request, formForm, user)
    else:
        return HttpResponseForbidden()


def formularioPublico(request, formForm, user):
    unresolved = formForm.isUnresolved() 
    if (request.method == "POST"):
        form = EvaluationFormForm(request, formForm)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/coordinacio/projectes/')
    else:
        form = EvaluationFormForm(request, formForm)
    plantilla = "formEvaluacion.html" if unresolved else "formularioPublico.html"
    return render_to_response(plantilla, locals())

@courseSelected
@eujierlogin_coordinator
def activarValoracion(request, user, course, alumnoid):
    student = QueryStudent().getStudentByUserUJI(alumnoid)
    if not student : return HttpResponseNotFound()
    
    project = QueryProject().getProjectByCourseAndStudent(course, student)
    if not project : return HttpResponseNotFound()
                                                 
    if not project.isUnresolved(): return HttpResponseForbidden()
    
    if (request.method == "POST"):
        activaValoracion(project)
        return HttpResponseRedirect('/coordinacio/projectes/')
    
    mensaje = u"Clica per a posar en curs l'evaluació de l'alumne " + student.nombreCompleto() + "."

    return render_to_response('mensajeValoracion.html', locals())

@courseSelected
@eujierlogin_coordinator
def reActivarValoracion(request, user, alumnoid, course, evaluacionid):
    student = QueryStudent().getStudentByUserUJI(alumnoid)
    if not student : return HttpResponseNotFound()
    project = QueryProject().getProjectByCourseAndStudent(course, student)
    if not project : return HttpResponseNotFound()
    evaluation = QueryEvaluation().getEvaluationByEvaluation(evaluacionid)
    if not evaluation : return HttpResponseNotFound()
    
    if not QueryForm().isFormCompletedOfProjectItemEvaluator(project, evaluation.getItem(), evaluation.getEvaluator()):
        return HttpResponseForbidden()
    
    if ( request.method == 'POST' ):
        #reActivaFormulario(project, evaluation)
        return HttpResponseRedirect('/coordinacio/projectes/')
    
    mensaje = u"Reactivar el formulari de l'evaluació " + unicode(evaluation) + " de " + unicode(evaluation.getItem()) + " de l'alumne " + student.nombreCompleto() + "."
    
    return render_to_response('mensajeValoracion.html', locals())