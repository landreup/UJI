from curso.models import Curso

from usuario.controllers import cambiaTutoresAProfesores

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
    return Curso.objects.order_by("-id")[0]

def cursoSeleccionado(request):
    if 'curso' in request.session:
        curso = request.session['curso']
    else:
        curso = ultimoCurso().curso
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
            curso = Curso(curso=curso)
            curso.save()
            cambiaTutoresAProfesores()
            return True
    return existe