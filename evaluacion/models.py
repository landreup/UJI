from django.db import models

from curso.models import Curso

class SistemaEvaluacion(models.Model):
    curso = models.ForeignKey(Curso)
    ESTADO_CHOICES = (
                     ('D', "Desactivat"),
                     ('A', 'Activat')
                     )
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)

    def __str__(self):
        return str(self.curso)
    
class Hito(models.Model):
    nombre = models.CharField(max_length=50)
    
    sistemaEvaluacion = models.ForeignKey(SistemaEvaluacion)
    plazo = models.IntegerField()
    orden = models.IntegerField()
          
    def __str__(self):
        return self.nombre
    
class Evaluacion(models.Model):
    nombre = models.CharField(max_length=50)
    hito = models.ForeignKey(Hito)
    EVALUADOR_CHOICES =  (
                         ('TU', "Tutor"),
                         ('S', "Supervisor"),
                         ('TR', "Tribunal"),
                         ('A', "Alumne")
                         )
    
    evaluador = models.CharField(max_length=2, choices=EVALUADOR_CHOICES)
    
    miembrosTribunal = models.IntegerField(null=True, blank=True)     
   
    def __str__(self):
        respuesta = ""
        for opcion in self.EVALUADOR_CHOICES :
            if (opcion[0] == self.evaluador):
                respuesta = opcion[1]
                break
        return self.nombre + " (" + respuesta + ")"
    
class Pregunta(models.Model):
    evaluacion = models.ForeignKey(Evaluacion)
    pregunta = models.CharField(max_length=100)
    TIPO_CHOICES = (
                    ('A', 'Apte/No Apte'),
                    ('I', 'Indicador de 1 a 5')
                    )
    tipoRespuesta = models.CharField(max_length=1, choices=TIPO_CHOICES)
       
    def __str__(self):
        respuesta = ""
        for opcion in self.TIPO_CHOICES :
            if (opcion[0] == self.tipoRespuesta):
                respuesta = opcion[1]
                break
        
        return self.pregunta + " ("+ respuesta + ")"