from django.forms import ModelForm

from models import Usuario
from usuario.queries import QueryUser

class UsuarioForm(ModelForm):
    class Meta():
        model = Usuario

class ProfesorForm():
    def __init__(self, request, accion="nuevo", profesorid=""):
        self.usuario = Usuario()
        self.accion = accion
        self.request= request
        self.profesorid = profesorid
        self.obligatorios = ["nombre", "apellidos", "usuarioUJI", "rol"]
        
        self.usuarioForm = UsuarioForm()
        if self.accion == "editar" :
            self.usuarioForm = UsuarioForm(instance = QueryUser().getUserByUserUJI(profesorid))
            
        if (request.method == "POST" ):
            self.usuarioForm = UsuarioForm(request.POST, instance=self.usuario)
            
    def is_valid(self):
        self.muestraErrorUsuario = True
        esValido = self.usuarioForm.is_valid()
        if ( not esValido and self.accion == "editar"):
            if ( self.usuarioForm.data["usuarioUJI"] == self.profesorid ):
                self.muestraErrorUsuario= False
                if len(self.usuarioForm.errors)==1:
                    esValido = True
                
        return esValido
    
    def save(self):
        if (self.accion == "nuevo"):
            self.creaUsuario()
        else:
            self.editaUsuario()
            
    def creaUsuario(self):
        self.usuario.save()
        
    def editaUsuario(self):
        usuarioDB = QueryUser().getUserByUserUJI(self.profesorid)
        usuarioDB.nombre = self.usuario.nombre
        usuarioDB.apellidos = self.usuario.apellidos
        usuarioDB.usuarioUJI = self.usuario.usuarioUJI
        usuarioDB.rol = self.usuario.rol
        usuarioDB.save()