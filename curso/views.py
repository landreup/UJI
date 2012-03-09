from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from curso.controllers import cursoNuevo, listaCursoTodos, creaCurso

def listadoCursos(request):
    campo =  "Cursos"
    listado = listaCursoTodos()
    anyadir = True
    return render_to_response('cursoListado.html', locals())

def nuevoCurso(request, confirma=False):
    curso = cursoNuevo()
    existe = False
    if (confirma):
        existe = creaCurso(curso)
        if (not existe) : return HttpResponseRedirect('/coordinacio/cursos')
    
    ocultaCurso = True
    return render_to_response('cursoNuevo.html', locals())