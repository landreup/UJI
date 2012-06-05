from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden

from forms import EvaluationFormForm
from queries import QueryEvaluationSystemTreeCompleteOfProject, QueryForm

from alumno.controllers import alumnoPorId
from curso.queries import QueryCourse
from proyecto.queries import QueryProject
from evaluacion.queries import QueryEvaluationSystem, QueryItem
from valoracion.controllers import activaFormulario, activaValoracion

from usuario.eujierlogin import eujierlogin, loginFromEujierlogin
from usuario.queries import QueryUser

@eujierlogin
def estadoValoracion(request, login, alumnoid):    
    evaluationSystem = QueryEvaluationSystem().getEvaluationSystemByCourseSelected(request)
    if not evaluationSystem:
        return HttpResponseNotFound()
    
    if not evaluationSystem.isActive():
        return HttpResponseNotFound()
    
    
    course = QueryCourse().getCourseSelected(request)
    student = alumnoPorId(alumnoid)
    project = QueryProject().getProjectByCourseAndStudent(course, student)
    coordinator = False
    if login != alumnoid :
        if login in QueryProject().getloginByRol(project, "TU"):
            rol = "TU"
        else:
            coordinator = QueryUser().getUserCoordinatorByUserUJI(login)
            rol = "C"
            if not coordinator : 
                return HttpResponseForbidden()

    if login == alumnoid :
        rol = "A"
    
    
    hitos = QueryEvaluationSystemTreeCompleteOfProject(project, True, rol).getList()
    
    
    student = login == alumnoid
    grupos = True
    activar=project.isUnresolved()
    cursoActual = True # Comprobar si curso actual
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
    if formForm.needUJIAuthentication() :
        access = False
        login = loginFromEujierlogin(request)
        if QueryProject().isUserRolinProject(formForm.proyecto, formForm.rol, login):
            access = True
        else:
            coordinador = QueryUser().getUserCoordinatorByUserUJI(login)
            if coordinador: access = True
            
    if access :
        return formularioPublico(request, formForm)
    else:
        return HttpResponseForbidden()

def formularioPublico(request, formForm):
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

def activarValoracion(request, alumnoid):
    course = QueryCourse().getCourseSelected(request)
    student = alumnoPorId(alumnoid)
    project = QueryProject().getProjectByCourseAndStudent(course, student)
    
    if not project.isUnresolved(): return HttpResponseForbidden()
    
    if (request.method == "POST"):
        activaValoracion(project)
        return HttpResponseRedirect('/coordinacio/projectes/')

    return render_to_response('activaValoracion.html', locals())
    