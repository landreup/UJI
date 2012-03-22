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
        self.obligatorios = ["nombre", "usuarioUJI", "rol"]
        
        if (form_action == "crea"):
            if (accion == "nuevo"):
                self.usuarioForm = UsuarioForm()
            else : # Edicion
                self.usuario = usuarioPorId(profesorid)
                self.usuario = self.usuario
                self.usuarioForm = UsuarioForm(initial = {
                                'nombre': self.usuario.nombre,
                                'usuarioUJI': self.usuario.usuarioUJI,
                                'rol': self.usuario.rol
                })
        else: # Leer
            if (request.method != "POST") : 
                # ERROR
                pass
            self.usuarioForm = UsuarioForm(request.POST, instance=self.usuario)
            
    def is_valid(self):
        esValido = self.usuarioForm.is_valid()
        if ( not esValido and self.accion == "editar"):
            if ( self.usuarioForm.data["usuarioUJI"] == self.profesorid ):
                esValido = True
        return esValido
    
    def save(self):
        if (self.accion == "nuevo"):
            creaUsuario(self.usuario)
        else:
            editaUsuario(self.profesorid, self.usuario)
