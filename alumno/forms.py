from django.forms import ModelForm

from models import Alumno

class AlumnoForm(ModelForm):
    class Meta():
        model = Alumno  