# -*- encoding: utf-8 -*-

from usuario.queries import QueryUser

def cambiaTutoresAProfesores():
    listadoTutores = QueryUser().getListOfTutor()
    for tutor in listadoTutores:
        tutor.rol="P"
        tutor.save()