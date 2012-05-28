# -*- encoding: utf-8 -*-
from django.shortcuts import get_object_or_404

from usuario.models import Usuario
from usuario.queries import QueryUser

def usuarioPorId(usuarioUJI):
    return get_object_or_404(Usuario, usuarioUJI=usuarioUJI)
    #return Usuario.objects.get(usuarioUJI=usuarioId)
    
def usuarioPorUsuario(usuario):
    return get_object_or_404(Usuario, id=usuario)

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

def cambiaTutoresAProfesores():
    listadoTutores = QueryUser().getListOfTutor()
    for tutor in listadoTutores:
        tutor.rol="P"
        tutor.save()