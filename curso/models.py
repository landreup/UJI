from django.db import models

class Curso(models.Model):
    curso = models.IntegerField()
    fechaTope = models.DateField(null=True, blank=True)
    esActual = False
    
    def __unicode__(self):
        return unicode(self.curso) + "/" + unicode(self.curso+1)