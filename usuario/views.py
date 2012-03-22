from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from forms import ProfesorForm
from controllers import listaCoordinador, listaTutor, listaProfesor, cambiarUsuario

def listadoProfesores(request):
    grupos = [
        {'campo': "Coordinadors", 'lista': listaCoordinador()},
        {'campo': "Tutors", 'lista': listaTutor()},
        {'campo': "Profesors", 'lista': listaProfesor()}
    ]
    anyadir = True
    editar = True
    return render_to_response('profesorListado.html', locals())

def gestionProfesor(request, accion="nuevo", profesorid=""):
    if (request.method == "POST" ) :
        form = ProfesorForm(request, accion, profesorid, "lee")
        if (form.is_valid()):
            form.save()
            #return HttpResponseRedirect('/coordinacio/professorat/')
    else:
        form = ProfesorForm(request, accion, profesorid)
    return render_to_response('profesorGestion.html', locals())

def cambiaUsuario(request, profesorid):
    cambiarUsuario(request, profesorid)
    return HttpResponseRedirect('/professorat/projectes/')
    