# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from forms import ProfesorForm

from eujierlogin import eujierlogin_coordinator
from usuario.queries import QueryUser

@eujierlogin_coordinator
def listadoProfesores(request, user):
    grupos = [
        {'campo': "Coordinadors", 'lista': QueryUser().getListOfCoordinator()},
        {'campo': "Tutors", 'lista': QueryUser().getListOfTutor()},
        {'campo': "Profesors", 'lista': QueryUser().getListOfProfessor()}
    ]
    anyadir = True
    editar = True
    return render_to_response('profesorListado.html', locals())

@eujierlogin_coordinator
def gestionProfesor(request, user, accion="nuevo", profesorid=""):
    if (request.method == "POST" ) :
        form = ProfesorForm(request, accion, profesorid, "lee")
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/coordinacio/professorat/')
    else:
        form = ProfesorForm(request, accion, profesorid)
    return render_to_response('profesorGestion.html', locals())    