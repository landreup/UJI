from django.forms import ModelForm

from models import Usuario
from controllers import usuarioPorId, creaUsuario, editaUsuario

class UsuarioForm(ModelForm):
    class Meta():
        model = Usuario

class ProfesorForm():
    def __init__(self, request, accion="nuevo", profesorid="", form_action="crea"):
        self.usuario = Usuario()
        self.accion = accion
        self.request= request
        self.profesorid = profesorid
        
        if (form_action == "crea"):
            if (accion == "nuevo"):
                self.usuarioForm = UsuarioForm()
            else : # Edicion
                self.usuario = usuarioPorId(profesorid)
                self.usuario = self.usuario[0]
                self.usuarioForm = UsuarioForm(initial = {
                                'nombre': self.profesor.nombre,
                                'usuarioUJI': self.profesor.usuarioUJI,
                                'rol': self.profesor.rol
                })
        else: # Leer
            if (request.method != "POST") : 
                # ERROR
                pass
            self.usuarioForm = UsuarioForm(request.POST, instance=self.usuario)
            
    def is_valid(self):
        return self.usuarioForm.is_valid()
    
    def save(self):
        if (self.accion == "nuevo"):
            creaUsuario(self.usuario)
        else:
            editaUsuario(self.profesorid, self.usuario)
