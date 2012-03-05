from alumno.models import Alumno

def alumnoPorId(alumnoid):
    return Alumno.objects.get(usuarioUJI=alumnoid)

def creaAlumno(alumno):
    alumno.save()

def editaAlumno(alumnoid, alumno):
    alumnoDB = alumnoPorId(alumnoid)
    alumnoDB.nombre = alumno.nombre
    alumnoDB.usuarioUJI = alumno.usuarioUJI
    alumnoDB.dni = alumno.dni
    alumnoDB.save()    