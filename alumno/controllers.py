from django.shortcuts import get_object_or_404
from alumno.models import Alumno

def alumnoPorId(usuarioUJI):
    return get_object_or_404(Alumno, usuarioUJI=usuarioUJI)
    #return Alumno.objects.get(usuarioUJI=alumnoid)

def alumnoPorAlumno(alumnoId):
    return get_object_or_404(Alumno, id=alumnoId)

def creaAlumno(alumno):
    alumno.save()

def editaAlumno(alumnoid, alumno):
    alumnoDB = alumnoPorId(alumnoid)
    alumnoDB.nombre = alumno.nombre
    alumnoDB.usuarioUJI = alumno.usuarioUJI
    alumnoDB.save()    