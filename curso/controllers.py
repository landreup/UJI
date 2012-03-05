from curso.models import Curso

from usuario.controllers import cambiaTutoresAProfesores

import datetime

def cambiarCurso(request):
    curso = Curso.objects.order_by("-id")[0]
    request.session['curso'] = curso

def listaCursoTodos():
    return Curso.objects.all().order_by("-id")

def cursoActual():
    return Curso.objects.order_by("-id")[0]

def cursoSeleccionado(request):
#    if 'curso' in request.session:
#        return request.session['curso']
#    else:
#        return cursoActual()
    return cursoActual()

def cursoNuevo():
    curso = int(datetime.date.today().year)
    return str(curso)+"/"+str(curso+1)

def existeCurso(curso):
    cursos = Curso.objects.filter(curso=curso)
    if (cursos):
        return True
    else:
        return False

def creaCurso(curso):
    existe = existeCurso(curso)
    if ( not existe ):
            curso = Curso(curso=curso)
            curso.save()
            cambiaTutoresAProfesores()
            return True
    return existe