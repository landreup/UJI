# coding: latin1
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden

from controllers import listaHitos, editable, activable, sistemaEvaluacionSeleccionado, copiarSistemaEvaluacionCursoAnteriorAlCursoActual
from forms import campoForm, EvaluationSystemForm

from curso.controllers import cambiarCurso

from curso.queries import QueryCourse

from usuario.eujierlogin import eujierlogin_coordinator

@eujierlogin_coordinator
def listadoHitos(request, user):
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

@eujierlogin_coordinator
def gestionEvaluaciones(request, user, accion="nuevo", campo= "", hito="", evaluacion="", pregunta=""):
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

@eujierlogin_coordinator
def activaSistemaEvaluacion(request, user):
    form = EvaluationSystemForm(request)
    if request.method == 'POST':
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/coordinacio/evaluacio/')
        
    return render_to_response('sistemaEvaluacionGestion.html', locals())

@eujierlogin_coordinator
def cambiaCurso(request, user, curso):
    cambiarCurso(request, curso)
    return HttpResponseRedirect(request.path.split('curs/')[0])    