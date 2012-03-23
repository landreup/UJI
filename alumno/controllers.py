from django.shortcuts import get_object_or_404
from alumno.models import Alumno

def alumnoPorId(alumnoid):
    return get_object_or_404(Alumno, usuarioUJI=alumnoid)
    #return Alumno.objects.get(usuarioUJI=alumnoid)

def creaAlumno(alumno):
    alumno.save()

def editaAlumno(alumnoid, alumno):
    alumnoDB = alumnoPorId(alumnoid)
    alumnoDB.nombre = alumno.nombre
    alumnoDB.usuarioUJI = alumno.usuarioUJI
    alumnoDB.save()    