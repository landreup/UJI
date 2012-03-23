from django.forms import ModelForm

from models import Proyecto
from alumno.models import Alumno

from alumno.forms import AlumnoForm

from alumno.controllers import alumnoPorId, creaAlumno, editaAlumno
from curso.controllers import cursoSeleccionado
from proyecto.controllers import proyectoPorId, creaProyecto, editaProyecto
from usuario.controllers import listaTutor

class ProyectoForm(ModelForm):
    class Meta():
        model = Proyecto
        exclude = ('curso', 'alumno')

class ProyectoAlumnoForm():
    def __init__(self, request, accion="nuevo", alumnoid="", form_action="crea"):
        self.alumno = Alumno()
        self.proyecto = Proyecto()
        self.accion = accion
        self.request = request
        self.alumnoid = alumnoid
        if (form_action == "crea"):
            if ( accion == "nuevo" ) :
                self.alumnoForm = AlumnoForm(prefix='alumno')
                self.proyectoForm = ProyectoForm(prefix='proyecto')
                self.proyectoForm.fields["tutor"].queryset = listaTutor()
            else: # Edicion
                self.alumno = alumnoPorId(alumnoid)
                
                self.alumnoForm = AlumnoForm(prefix='alumno', initial={
                            'nombre': self.alumno.nombre, 
                            'apellidos': self.alumno.apellidos,
                            'usuarioUJI': self.alumno.usuarioUJI
                })
                
                self.proyecto = proyectoPorId(self.alumno, cursoSeleccionado(request))
            
                self.proyectoForm = ProyectoForm(prefix='proyecto', initial={
                            'tutor': self.proyecto.tutor, 
                            'supervisor': self.proyecto.supervisor,
                            'email': self.proyecto.email, 
                            'empresa': self.proyecto.empresa, 
                            'telefono': self.proyecto.telefono,
                            'titulo': self.proyecto.titulo,
                            'inicio': self.proyecto.inicio,
                            'dedicacionSemanal': self.proyecto.dedicacionSemanal,
                            'otrosDatos': self.proyecto.otrosDatos
                })
                self.proyectoForm.fields["tutor"].queryset = listaTutor()
                self.proyectoForm.initial["tutor"] = self.proyecto.tutor
        else: # Leer
            if (request.method != "POST") : 
                # ERROR
                pass
            self.alumnoForm = AlumnoForm(request.POST, prefix='alumno', instance=self.alumno)
            self.proyectoForm = ProyectoForm(request.POST, prefix='proyecto', instance=self.proyecto)
                
                
    def is_valid(self):
        alumnoEsValido = self.alumnoForm.is_valid()
        if ( not alumnoEsValido and self.accion == "editar"):
            alumnoEsValido =True
            if ( self.alumnoForm.data["usuarioUJI"] == self.alumnoid ):
                alumnoEsValido = True
        
        return (alumnoEsValido and self.proyectoForm.is_valid())
    
    def getAlumnoProyecto(self):
        return self.alumno, self.proyecto
    
    def getAlumnoId(self):
        return self.alumnoid
    
    def getAccion(self):
        return self.accion
    
    def save(self):
        if (self.accion == "nuevo"):
                creaAlumno(self.alumno)
                creaProyecto(self.request, self.proyecto, self.alumno)
        else : # edicion
                editaAlumno(self.alumnoid, self.alumno)
                editaProyecto(self.request, self.alumno, self.proyecto)
