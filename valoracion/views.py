from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse

from forms import FormForm, EvaluationFormForm
from queries import QueryEvaluationSystemTreeCompleteOfProject, QueryForm

from alumno.controllers import alumnoPorId
from curso.controllers import cursoSeleccionado
from proyecto.queries import QueryProject
from evaluacion.forms import EvaluationForm


def estadoValoracion(request, alumnoid):
    course = cursoSeleccionado(request)
    student = alumnoPorId(alumnoid)
    project = QueryProject().getProjectByCourseAndStudent(course, student)
    hitos = QueryEvaluationSystemTreeCompleteOfProject(project, True).getList()
    
    grupos = True
    return render_to_response("sistemaEvaluacionValoradoListado.html", locals())

def creaFormulario(request, alumnoid, hitoid):
    # Comprobar acceso
    
    if (request.method == "POST"):
        form = FormForm(request, alumnoid, hitoid)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/coordinacio/projectes/')
    else:
        form = FormForm(request, alumnoid, hitoid)
        
    return render_to_response('creaFormulario.html', locals())

def formularioPublico(request, clave):
    # Comprobar acceso
    
    formForm = QueryForm().getFormByKey(clave)
    if (request.method == "POST"):
        form = EvaluationFormForm(request, formForm)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/coordinacio/projectes/')
            
    else:
        form = EvaluationFormForm(request, formForm)
    return render_to_response('formularioPublico.html', locals())
    
    #form = EvaluationFormForm(request, form)
    #if (request.method == "POST"):
    #    form = FormForm(request, alumnoid, hitoid)
    #    if (form.is_valid()):
    #        form.save()
    #        return HttpResponseRedirect('/coordinacio/projectes/')
    #else:
    #    form = FormForm(request, alumnoid, hitoid)
    #    
    #return render_to_response('creaFormulario.html', locals())