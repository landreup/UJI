from django.db import models

from proyecto.models import Proyecto
from evaluacion.models import Hito, Evaluacion, Pregunta
from evaluacion.queries import QueryEvaluation

class Formulario(models.Model):
    proyecto = models.ForeignKey(Proyecto)
    hito = models.ForeignKey(Hito)
    rol = models.CharField(max_length=2)
    idMiembro = models.IntegerField(null=True, blank=True)
    codigo = models.CharField(max_length=100, unique=True)
    fechaValorado = models.DateTimeField(null=True, blank=True)
    
    def isUnresolved(self):
        return self.proyecto.isUnresolved()
    
    def isCompleted(self):
        if self.fechaValorado : return True
        else : return False
    
    def needUJIAuthentication(self):
        return self.rol != "S"
    
    def __unicode__(self):
        roles = QueryEvaluation().getRoles()
        cadena = u"Formulari de " + unicode(self.hito).lower() + u" de " + roles[self.rol] + u" de " + self.proyecto.alumno.nombreCompleto
        cadena += " en " + self.fechaValorado.strftime('%d/%m/%Y - %H:%M') if self.fechaValorado else ""
        return cadena
    
    class Meta:
        unique_together= [("proyecto", "hito", "rol", "idMiembro", 'fechaValorado')]

class EvaluacionesFormulario(models.Model):
    evaluacion = models.ForeignKey(Evaluacion)
    formulario = models.ForeignKey(Formulario)
    valoracionEvaluacion = models.FloatField(null=True, blank=True) 

class Valoracion(models.Model):
    pregunta = models.ForeignKey(Pregunta)
    respuesta = models.IntegerField()
    evaluacionFormulario = models.ForeignKey(EvaluacionesFormulario)