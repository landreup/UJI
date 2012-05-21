from django.db import models

class Alumno(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    usuarioUJI = models.CharField(max_length=30, unique=True)
    
    def __unicode__(self):
        return self.apellidos + ", " + self.nombre
    
    def nombreCompleto(self):
        return self.nombre + " " + self.apellidos
    class Meta:
        ordering = ["apellidos"]
