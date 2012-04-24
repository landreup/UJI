# coding: latin1
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden

from controllers import listaHitos, editable, sistemaEvaluacionSeleccionado, copiarSistemaEvaluacionCursoAnteriorAlCursoActual
from forms import campoForm

from curso.controllers import listaCurso, cambiarCurso

def listadoHitos(request):
    if request.method == 'POST':
        if not editable():
            return HttpResponseForbidden
        copiarSistemaEvaluacionCursoAnteriorAlCursoActual(request)
        return HttpResponseRedirect('/coordinacio/evaluacio/')
    
    sistemaEvaluacion = sistemaEvaluacionSeleccionado(request)
       
    hitos = listaHitos(sistemaEvaluacion) if (sistemaEvaluacion) else []
    
    cursos = listaCurso(request)
    grupos = True
    edita = editable(request)
    anyadir = sistemaEvaluacion
    return render_to_response('sistemaEvaluacionListado.html', locals())

def gestionEvaluaciones(request, accion="nuevo", campo= "", hito="", evaluacion="", pregunta=""):
    if not editable(request):
        return HttpResponseForbidden()
    
    if (request.method == 'POST'):
        form = campoForm(request, accion, campo, hito, evaluacion, pregunta, "lee")
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/coordinacio/evaluacio/')
        form = form.getForm()
    else:
        form = campoForm(request, accion, campo, hito, evaluacion, pregunta).getForm()
    return render_to_response(campo+'Gestion.html', locals())

def cambiaCurso(request, curso):
    cambiarCurso(request, curso)
    return HttpResponseRedirect(request.path.split('curs/')[0])    