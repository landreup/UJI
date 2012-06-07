from django.db import models

class Curso(models.Model):
    curso = models.IntegerField()
    fechaTope = models.DateField(null=True, blank=True)
    esActual = False
    
    def getFechaTope(self):
        return unicode(self.fechaTope)
    
    def __unicode__(self):
        return unicode(self.curso) + "/" + unicode(self.curso+1) + " - " + unicode(self.fechaTope)