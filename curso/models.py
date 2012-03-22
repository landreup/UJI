from django.db import models

class Curso(models.Model):
    curso = models.CharField(max_length=15)
    esActual = False
    
    def __str__(self):
        return self.curso