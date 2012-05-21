# coding: latin1
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden

from controllers import listaHitos, editable, activable, sistemaEvaluacionSeleccionado, copiarSistemaEvaluacionCursoAnteriorAlCursoActual
from forms import campoForm, EvaluationSystemForm

from curso.controllers import cambiarCurso

from curso.queries import QueryCourse

def listadoHitos(request):
    if request.method == 'POST':
        if not editable(request):
            return HttpResponseForbidden
        copiarSistemaEvaluacionCursoAnteriorAlCursoActual(request)
        return HttpResponseRedirect('/coordinacio/evaluacio/')
    
    sistemaEvaluacion = sistemaEvaluacionSeleccionado(request)
       
    hitos = listaHitos(sistemaEvaluacion) if (sistemaEvaluacion) else []
    
    cursos = QueryCourse().getListCourse(request)
    grupos = True
    edita = editable(request)
    anyadir = sistemaEvaluacion
    activar = activable(request)
    return render_to_response('sistemaEvaluacionListado.html', locals())

def gestionEvaluaciones(request, accion="nuevo", campo= "", hito="", evaluacion="", pregunta=""):
    if not editable(request):
        return HttpResponseForbidden()
    
    if (request.method == 'POST'):
        form = campoForm(request, accion, campo, hito, evaluacion, pregunta)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/coordinacio/evaluacio/')
        form = form.getForm()
    else:
        form = campoForm(request, accion, campo, hito, evaluacion, pregunta).getForm()
    return render_to_response(campo+'Gestion.html', locals())

def activaSistemaEvaluacion(request):
    form = EvaluationSystemForm(request)
    if request.method == 'POST':
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/coordinacio/evaluacio/')
        
    return render_to_response('sistemaEvaluacionGestion.html', locals())

def cambiaCurso(request, curso):
    cambiarCurso(request, curso)
    return HttpResponseRedirect(request.path.split('curs/')[0])    