# -*- encoding: utf-8 -*-

from django.forms import ModelForm

from models import Proyecto
from queries import QueryProject

from alumno.models import Alumno

from alumno.forms import AlumnoForm

from alumno.controllers import alumnoPorId
from curso.controllers import cursoSeleccionado
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
                
                self.proyecto = QueryProject().getProjectByCourseAndStudent(cursoSeleccionado(request), self.alumno)
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
            self.createProjectStudent()
        else : # edicion
            self.editProjectStudent()
    
    def createProjectStudent(self):
        self.createStudent()
        self.createProject()
    
    def createStudent(self):
        self.alumno.save()
    
    def createProject(self):
        self.proyecto.alumno = self.alumno
        self.proyecto.curso = cursoSeleccionado(self.request)
        self.proyecto.save()

    def editProjectStudent(self):
        self.editStudent()
        self.editProject()
    
    def editStudent(self):
        alumnoDB = alumnoPorId(self.alumnoid)
        alumnoDB.nombre = self.alumno.nombre
        alumnoDB.usuarioUJI = self.alumno.usuarioUJI
        alumnoDB.save()
        
    def editProject(self):
        curso = cursoSeleccionado(self.request)
    
        proyectoDB = proyectoPorId(self.alumno, curso)
    
        proyectoDB.tutor = self.proyecto.tutor
        proyectoDB.supervisor = self.proyecto.supervisor
        proyectoDB.email = self.proyecto.email
        proyectoDB.empresa = self.proyecto.empresa
        proyectoDB.telefono = self.proyecto.telefono
        proyectoDB.titulo = self.proyecto.titulo
        proyectoDB.inicio = self.proyecto.inicio
        proyectoDB.dedicacionSemanal = self.proyecto.dedicacionSemanal
        proyectoDB.otrosDatos = self.proyecto.otrosDatos
    
        proyectoDB.save()