from usuario.forms import ProfesorForm
from django.http import HttpResponseRedirect, HttpResponseNotFound,\
    HttpResponseForbidden
from django.shortcuts import render_to_response
from curso.controllers import cursoNuevo
from curso.models import Curso
from evaluacion.models import SistemaEvaluacion
from usuario.eujierlogin import eujierlogin
import datetime
from alumno.queries import QueryStudent
from usuario.queries import QueryUser
from curso.queries import QueryCourse

@eujierlogin
def iniciaAplicacion(request, login):
    if QueryCourse().getLastCourse():
        return HttpResponseForbidden()
    
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

@eujierlogin
def index(request, login):
    teacher = QueryUser().getUserByUserUJI(login)
    if teacher :
        if teacher.isCoordinator():
            return HttpResponseRedirect('/coordinacio/projectes/')
        else:
            return HttpResponseRedirect('/professorat/projectes/')
        
    student = QueryStudent().getStudentByUserUJI(login)
    if student:
        return HttpResponseRedirect('/valoracio/'+login+'/')
    else:
        return HttpResponseNotFound()
        