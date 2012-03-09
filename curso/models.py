from django.db import models

class Curso(models.Model):
    curso = models.CharField(max_length=15)
    
    def __str__(self):
        return self.curso
    
    def get(self, campo):
        if (campo=="curso"): return self.curso
        return ""