# -*- coding: utf-8 -*-

from django.db import models

from alumno.models import Alumno
from curso.models import Curso
from usuario.models import Usuario
from evaluacion.models import Hito

class Proyecto(models.Model):
    alumno = models.ForeignKey(Alumno, null=True)
    tutor = models.ForeignKey(Usuario)
    supervisor = models.CharField(max_length=100, null=True)
    email = models.EmailField()
    curso = models.ForeignKey(Curso)
    
    empresa= models.CharField(max_length=100)
    telefono = models.CharField(max_length=9)
    
    titulo = models.CharField(max_length=200, null=True, blank=True)
    
    inicio = models.DateField(null=True, blank=True)
    dedicacionSemanal = models.FloatField(null=True, blank=True)
    
    otrosDatos = models.TextField(blank=True, null=True)
    
    ESTADO_CHOICES = (
                    ('P', 'Pendiente'),
                    ('E', 'En curso'),
                    ('F', 'Finalizado')
                    )
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    
    def __unicode__(self):
        return self.titulo        
    
    class Meta:
        unique_together = [("alumno", "curso")]
        ordering = ["alumno"]
    
    def isUnresolved(self):
        return self.estado == "P"
    
class MiembroTribunal(models.Model):
    proyecto = models.ForeignKey(Proyecto)
    idMiembro = models.IntegerField()
    miembro = models.ForeignKey(Usuario)
    
    def __unicode__(self):
        return unicode(self.idMiembro) + ".- " + unicode(self.miembro) + " - " + unicode(self.proyecto)
    
    class Meta:
        unique_together = [("proyecto", "idMiembro")]

class FechaEstimada(models.Model):
    proyecto = models.ForeignKey(Proyecto)
    hito = models.ForeignKey(Hito)
    fecha = models.DateField()
    
    class Meta:
        unique_together = [("proyecto", "hito")]
        
class EstadoProyectoEnCurso(models.Model):
    proyecto = models.ForeignKey(Proyecto)
    hito = models.ForeignKey(Hito)
    
class ProyectoParaRevisionEnCurso(models.Model):
    proyecto = models.ForeignKey(Proyecto)
    campos = models.TextField()
