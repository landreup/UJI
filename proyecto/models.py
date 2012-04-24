# -*- coding: utf-8 -*-

from django.db import models

from alumno.models import Alumno
from curso.models import Curso
from usuario.models import Usuario

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
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        unique_together = [("alumno", "curso")]
        order_with_respect_to = "alumno"