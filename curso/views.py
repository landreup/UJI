from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseNotFound

from curso.controllers import cursoNuevo, creaCurso
from curso.queries import QueryCourse
from curso.models import Curso
from curso.forms import CursoForm

def listadoCursos(request):
    campo =  "Cursos"
    listado = QueryCourse().getListCourse(request)
    anyadir = True
    return render_to_response('cursoListado.html', locals())

def nuevoCurso(request, confirma=False):
    curso = cursoNuevo()
    existe = False
    if (confirma):
        creado = creaCurso(curso)
        if (creado) : return HttpResponseRedirect('/coordinacio/cursos/')
    
    ocultaCurso = True
    return render_to_response('cursoNuevo.html', locals())

def editaCurso(request, curso):
    cursoA = int(curso.split("/")[0])
    cursoB = int(curso.split("/")[1])
    if cursoA+1 != cursoB :  return HttpResponseNotFound()
    curso = cursoA
    
    cursoForm = Curso()
    cursoDB = QueryCourse().getCourseByCourse(curso)
    
    if not cursoDB : return HttpResponseNotFound()
    
    if (request.method == "POST") :
        form = CursoForm(request.POST, instance=cursoForm)
        if form.is_valid():
            cursoDB.fechaTope = cursoForm.fechaTope
            cursoDB.save()
            return HttpResponseRedirect('/coordinacio/cursos/')
    else:
        form = CursoForm(initial={'fechaTope':cursoDB.fechaTope})
    
    return render_to_response('edicionCurso.html', locals())