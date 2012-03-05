from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from forms import ProfesorForm
from controllers import listaCoordinador, listaTutor, listaProfesor

def listadoProfesores(request):
    listadoCoordinadores = listaCoordinador()
    listadoTutores = listaTutor()
    listadoProfesores = listaProfesor()
    return render_to_response('profesorListado.html', {'listaCoordinadores': listadoCoordinadores, 'listaTutores': listadoTutores, 'listaProfesores': listadoProfesores})

def gestionProfesor(request, accion="nuevo", profesorid=""):
    #profesorid = profesorid if (profesorid[-1]!='/') else profesorid[:-1]
    if (request.method == "POST" ) :
        form = ProfesorForm(request, accion, profesorid, "lee")
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/coordinacio/professorat')
    else:
        form = ProfesorForm(request, accion, profesorid)
    
    # CAMBIAR PLANTILLA PARA QUE RECIBA SOLO UN FORMULARIO
    return render_to_response('profesorGestion.html', {'form': form.usuarioForm, 'accion': accion, 'professorid': profesorid})
