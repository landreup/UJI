from django.shortcuts import get_object_or_404
from models import Proyecto

from alumno.controllers import alumnoPorAlumno
from curso.controllers import cursoSeleccionado
from usuario.controllers import usuarioActivo, usuarioPorId, usuarioPorUsuario

class QueryProject():
    def getProjectByCourseAndStudent(self, course, student):
        return get_object_or_404(Proyecto, alumno=student, curso=course)
    
    def getListProjectByCourse(self, course):
        return Proyecto.objects.filter(curso=course)
    
    def getListProjectByCourseSelected(self, request):
        return self.getListProjectByCourse(cursoSeleccionado(request))
    
    def getListProjectByCourseAndTutor(self, course, tutor):
        return Proyecto.objects.filter(curso=course, tutor=tutor)
    
    def getListProjectByCourseSelectedAndTutorSelected(self, request):
        return self.getListProjectByCourseSelected(request)
    
    def getListProjectByCourseSelectedAndTutorUserUJI(self, request, tutorUserUJI):
        tutor = usuarioPorId(tutorUserUJI)
        return self.getListProjectByCourseAndTutor(cursoSeleccionado(request), tutor)
    
    def getEmailByProjectAndEvaluator(self, project, rol):
        if rol == "A" :
            student = project.alumno
            return student.usuarioUJI + "@uji.es"
        elif rol == "TU" :
            user = project.tutor
            return user.usuarioUJI + "@uji.es"
        elif rol == "S" :
            return project.email
        elif rol == "TR" :
            return "a\@b.es"
        else:
            return "a\@a.es"
            