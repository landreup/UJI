from curso.models import Curso

from usuario.controllers import cambiaTutoresAProfesores
from proyecto.controllers import copiaProyectosEnCursoCursoActualAProyectosPendientesCursoNuevo

import datetime

def cambiarCurso(request, curso):
    curso = int(curso.split("/")[0])
    curso = Curso.objects.get(curso=curso)
    request.session['curso'] = curso

def cursoNuevo():
    curso = int(datetime.date.today().year)
    curso += 1
    return str(curso)+"/"+str(curso+1)

def existeCurso(curso):
    cursos = Curso.objects.filter(curso=curso)
    if (cursos):
        return True
    else:
        return False

def creaCurso(curso):
    curso = int(curso.split("/")[0])
    existe = existeCurso(curso)
    creado = False
    if ( not existe ):
            curso = Curso(curso=curso)
            curso.save()
            cambiaTutoresAProfesores()
            copiaProyectosEnCursoCursoActualAProyectosPendientesCursoNuevo(curso)
            #evaluationSystemCopy = EvaluationSystemCopy().fromCourse(cursoAnterior).toNewEvaluationSystemInCourse(curso)
            creado =  True
    return creado