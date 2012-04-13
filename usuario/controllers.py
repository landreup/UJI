# coding: latin1

from django.shortcuts import get_object_or_404

from usuario.models import Usuario

def usuarioPorId(usuarioId):
    return get_object_or_404(Usuario, usuarioUJI=usuarioId)
    #return Usuario.objects.get(usuarioUJI=usuarioId)

def cambiarUsuario(request, usuarioid):
    usuario = usuarioPorId(usuarioid)
    request.session['usuario'] = usuario

def usuarioActivo(request):
    return request.session['usuario']

def creaUsuario(usuario):
    usuario.save()

def editaUsuario(usuarioId, usuario):
    usuarioDB = usuarioPorId(usuarioId)
    usuarioDB.nombre = usuario.nombre
    usuarioDB.usuarioUJI = usuario.usuarioUJI
    usuarioDB.rol = usuario.rol
    usuarioDB.save()

def nombreTutor(usuarioId):
    return usuarioPorId(usuarioId).nombre

def usuarioPorRol(rol):
    return Usuario.objects.filter(rol=rol).order_by("apellidos")

def listaCoordinador():
    return usuarioPorRol("C")

def listaTutor():
    return usuarioPorRol("T")

def listaProfesor():
    return usuarioPorRol("P")

def cambiaTutoresAProfesores():
    listadoTutores = listaTutor()
    for tutor in listadoTutores:
        tutor.rol="P"
        tutor.save()