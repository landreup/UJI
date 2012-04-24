# -*- encoding: utf-8 -*-

from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    usuarioUJI = models.CharField(max_length=30, unique=True)
    ROL_CHOICES = (
                    ('P', 'Professor'),
                    ('T', 'Tutor'),
                    ('C', 'Coordinador')
                    )
    rol = models.CharField(max_length=1, choices=ROL_CHOICES)
    
    def __str__(self):
        return u'%s, %s'%(self.apellidos,self.nombre)
    
    def __unicode__(self): 
        return u'%s, %s'%(self.apellidos,self.nombre)
    
    class Meta:
        ordering = ["apellidos"]
