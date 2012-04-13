from curso.models import Curso

from usuario.controllers import cambiaTutoresAProfesores

#from evaluacion.controllers import editable

import datetime

def cambiarCurso(request, curso):
    curso = Curso.objects.get(curso=curso)
    request.session['curso'] = curso

def listaCurso(request):
    cursos = Curso.objects.all().order_by("-id")
    
    cursoSelec = cursoSeleccionado(request)
    
    for curso in cursos:
        if ( curso.curso == cursoSelec.curso ) :
            curso.esActual = True
    return cursos

def esCursoActual(request):
    return  ultimoCurso() == cursoSeleccionado(request)

def ultimoCurso():
    cursos = Curso.objects.order_by("-id")
    if cursos :
        return cursos[0]
    else:
        return []

def cursoSeleccionado(request):
    if 'curso' in request.session:
        curso = request.session['curso']
    else:
        curso = ultimoCurso()
        request.session['curso'] = curso
    return curso

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
            cursoAnterior = ultimoCurso()
            curso = Curso(curso=curso)
            curso.save()
            cambiaTutoresAProfesores()
            #evaluationSystemCopy = EvaluationSystemCopy().fromCourse(cursoAnterior).toNewEvaluationSystemInCourse(curso)
            return True
    return existe