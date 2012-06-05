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
    
    def getRoles(self):
        roles = {}
        for rol in self.ROL_CHOICES:
            roles[rol[0]] = rol[1]
        return roles
    
    def isCoordinator(self):
        return self.rol == "C"
    
    def esCoordinador(self):
        return self.isCoordinator()
    
    def isTutor(self):
        return self.rol == "T" or self.rol == "C"
    
    def esTutor(self):
        return self.isTutor()
    
    def getMail(self):
        return self.usuarioUJI + "@uji.es"
    
    def __str__(self):
        return u'%s, %s'%(self.apellidos,self.nombre)
    
    def __unicode__(self): 
        return u'%s, %s'%(self.apellidos,self.nombre)
    
    class Meta:
        ordering = ["apellidos"]
