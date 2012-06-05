from django.db import models

from curso.models import Curso

class SistemaEvaluacion(models.Model):
    curso = models.ForeignKey(Curso)
    ESTADO_CHOICES = (
                     ('D', "Desactivat"),
                     ('A', 'Activat')
                     )
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)

    def __unicode__(self):
        return unicode(self.curso)
    
    def isActive(self):
        return self.estado == "A"
    
class Hito(models.Model):
    nombre = models.CharField(max_length=50)
    
    sistemaEvaluacion = models.ForeignKey(SistemaEvaluacion)
    plazo = models.IntegerField()
    orden = models.IntegerField()
          
    def __unicode__(self):
        return self.nombre
    
class Evaluacion(models.Model):
    nombre = models.CharField(max_length=50)
    hito = models.ForeignKey(Hito)
    porcentaje = models.FloatField()
    EVALUADOR_CHOICES =  (
                         ('TU', "Tutor"),
                         ('S', "Supervisor"),
                         ('TR', "Tribunal"),
                         ('A', "Alumne"),
                         ('C', 'Coordinador')
                         )
    
    evaluador = models.CharField(max_length=2, choices=EVALUADOR_CHOICES)     
   
   
    def getPercentage(self):
        return self.porcentaje
   
    def getRoles(self):
        roles = dict()
        for rol in self.EVALUADOR_CHOICES:
            roles[rol[0]] = rol[1]
        return roles

    def __unicode__(self):
        roles = self.getRoles()
        evaluador = roles[self.evaluador]
        cadena = u"%s (%s) %0.1f"%(self.nombre, evaluador, self.porcentaje)
        cadena += "%"
        return cadena
    
    def isTribunalEvaluator(self):
        return self.evaluador == "TR"
    
class Pregunta(models.Model):
    evaluacion = models.ForeignKey(Evaluacion)
    pregunta = models.CharField(max_length=100)
    TIPO_CHOICES = (
                    ('A', 'Apte/No Apte'),
                    ('I', 'Indicador de 1 a 5')
                    )
    tipoRespuesta = models.CharField(max_length=1, choices=TIPO_CHOICES)
    
    def getTipeQuestion(self):
        tipeQuestion = dict()
        for tipe in self.TIPO_CHOICES :
            tipeQuestion[tipe[0]] = tipe[1]
        return tipeQuestion
    
    def __unicode__(self):
        tipeQuestion = self.getTipeQuestion()
        respuesta = tipeQuestion[self.tipoRespuesta]
        return  u"%s (%s)"%(self.pregunta, respuesta)