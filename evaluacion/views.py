# coding: latin1
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden

from controllers import listaHitos, editable
from forms import campoForm

from curso.controllers import listaCurso

def listadoHitos(request):
    hitos = listaHitos(request)
    
    cursos = listaCurso(request)
    grupos = True
    edita = editable(request)
    anyadir = edita
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