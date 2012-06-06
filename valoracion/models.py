from django.db import models

from proyecto.models import Proyecto
from evaluacion.models import Hito, Evaluacion, Pregunta

class Formulario(models.Model):
    proyecto = models.ForeignKey(Proyecto)
    hito = models.ForeignKey(Hito)
    rol = models.CharField(max_length=2)
    idMiembro = models.IntegerField(null=True, blank=True)
    codigo = models.CharField(max_length=100, unique=True)
    fechaValorado = models.DateField(null=True, blank=True)
    fechaBloqueado = models.DateField(null=True, blank=True)
    
    def isUnresolved(self):
        return self.proyecto.isUnresolved()
    
    def needUJIAuthentication(self):
        return self.rol != "S"
    
    def __unicode__(self):
        return "Valorar " + unicode(self.hito).lower() + " de " + self.proyecto.alumno.nombre + " " + self.proyecto.alumno.apellidos
    
    class Meta:
        unique_together= [("proyecto", "hito", "rol", "idMiembro")]

class EvaluacionesFormulario(models.Model):
    evaluacion = models.ForeignKey(Evaluacion)
    formulario = models.ForeignKey(Formulario)
    valoracionEvaluacion = models.FloatField(null=True, blank=True) 

class Valoracion(models.Model):
    pregunta = models.ForeignKey(Pregunta)
    respuesta = models.IntegerField()
    evaluacionFormulario = models.ForeignKey(EvaluacionesFormulario)