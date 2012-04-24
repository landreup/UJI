from django.db import models

from proyecto.models import Proyecto
from evaluacion.models import Evaluacion, Pregunta

class Formulario(models.Model):
    proyecto = models.ForeignKey(Proyecto)
    email = models.EmailField()
    codigo = models.CharField(max_length=100, unique=True)
    fechaEstimada = models.DateField()
    fechaValorado = models.DateField(null=True, blank=True)
    fechaBloqueado = models.DateField(null=True, blank=True)
    
    class Meta:
        unique_together= [("proyecto", "fechaEstimada", "email")]

class EvaluacionesFormulario(models.Model):
    evaluacion = models.ForeignKey(Evaluacion)
    formulario = models.ForeignKey(Formulario)

class Valoracion(models.Model):
    pregunta = models.ForeignKey(Pregunta)
    respuesta = models.IntegerField()
    evaluacionFormulario = models.ForeignKey(EvaluacionesFormulario)