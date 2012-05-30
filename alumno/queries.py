from alumno.models import Alumno
class QueryStudent():
    def getStudentByUserUJI(self, userUJI):
        try:
            return Alumno.objects.get(usuarioUJI=userUJI)
        except Alumno.DoesNotExist:
            return None