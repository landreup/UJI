from usuario.forms import ProfesorForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from curso.controllers import cursoNuevo
from curso.models import Curso
from evaluacion.models import SistemaEvaluacion
from usuario.eujierlogin import eujierlogin
import datetime

@eujierlogin
def iniciaAplicacion(request, login):
    if (request.method == "POST" ) :
        form = ProfesorForm(request)
        if (form.is_valid()):
            form.save()
            curso = Curso(curso=int(datetime.date.today().year))
            curso.save()
            newEvaluationSystem = SistemaEvaluacion(curso=curso, estado="D")
            newEvaluationSystem.save()
            return HttpResponseRedirect('/coordinacio/projectes/')
    else:
        form = ProfesorForm(request)
    return render_to_response('inicializaAplicacion.html', locals()) 