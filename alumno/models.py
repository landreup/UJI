from django.db import models

class Alumno(models.Model):
    nombre = models.CharField(max_length=50)
    usuarioUJI = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.nombre