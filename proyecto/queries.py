from models import Proyecto, MiembroTribunal, FechaEstimada, EstadoProyectoEnCurso

from curso.queries import Course
from usuario.queries import QueryUser
from proyecto.models import ProyectoParaRevisionEnCurso
from valoracion.queries import QueryForm

class QueryProject():
    def getProjectByCourseAndStudent(self, course, student):
        try:
            return Proyecto.objects.get(alumno=student, curso=course)
        except Proyecto.DoesNotExist:
            return None
    
    def getListProjectByCourse(self, course):
        return Proyecto.objects.filter(curso=course)
    
    def getListProjectByCourseSelected(self, request):
        return self.getListProjectByCourse(Course().getByCourseSelected(request))
    
    def getListProjectByCourseAndStatus(self, course, status):
        return Proyecto.objects.filter(estado=status, curso=course)
    
    def getListProjectInCourseByCourse(self, course):
        listProjects = []
        for project in self.getListProjectByCourseAndStatus(course, "C"):
            listProjects.append(project)
        
        for project in self.getListProjectByCourseAndStatus(course, "L"):
            listProjects.append(project)
        
        return listProjects 
    
    def getListProjectByCourseSelectedStatus(self, request, status):
        return self.getListProjectByCourseAndStatus(Course().getByCourseSelected(request), status)    
    
    def getListProjectByCourseStatusTutor(self, course, status, tutor):
        return Proyecto.objects.filter(estado=status, curso=course, tutor=tutor)
    
    def getListProjectByCourseSelectedStatusTutor(self, request, status, tutor):
        return self.getListProjectByCourseAndStatus(Course().getByCourseSelected(request), status, tutor)    
    
    def getListProjectByCourseAndTutor(self, course, tutor):
        return Proyecto.objects.filter(curso=course, tutor=tutor)
    
    def getListProjectByCourseSelectedAndTutorSelected(self, request):
        return self.getListProjectByCourseSelected(request)
    
    def getListProjectByCourseSelectedAndTutorUserUJI(self, request, tutorUserUJI):
        tutor = QueryUser().getUserByUserUJI(tutorUserUJI)
        return self.getListProjectByCourseAndTutor(Course().getByCourseSelected(request), tutor)
    
    def getloginByRol(self, project, rol):
        if rol == "A":
            yield project.alumno.usuarioUJI
        elif rol == "TU":
            yield project.tutor.usuarioUJI
        elif rol == "C":
            coordinators = QueryUser().getListOfCoordinator()
            for coordinator in coordinators:
                yield coordinator.usuarioUJI
        elif "TR" in rol:
            listTribunal = QueryJudgeMembers().getListMembersByProject(project)
            for member in listTribunal:
                yield member.miembro.usuarioUJI
        else:
            yield None
        
    
    def getEmailByProjectAndEvaluator(self, project, rol):
        if rol != "S":
            for user in self.getloginByRol(project, rol):
                yield user + "@uji.es" 
        else:
            yield project.email
    
    def isUserRolinProject(self, project, rol, login):
        return login in self.getloginByRol(project, rol)
        
class QueryJudgeMembers():
    def getListMembersByProject(self, project):
        return MiembroTribunal.objects.filter(proyecto=project).order_by("idMiembro")
    
    def getJudgeMemberByProjectAndMemberId(self, project, memberId):
        try:
            return MiembroTribunal.objects.get(proyecto=project, idMiembro=memberId)
        except MiembroTribunal.DoesNotExist:
            return None
    
    def isJudgeDefinedForProject(self, project):
        return len(self.getListMembersByProject(project)) == 3
    
class QueryEstimateDate():
    def getListEstimateDateByProject(self, project):
        return FechaEstimada.objects.filter(proyecto=project)
    
    def getEstimateDateByProjectAndItem(self, project, item):
        try:
            return FechaEstimada.objects.get(proyecto=project, hito=item)
        except FechaEstimada.DoesNotExist:
            return None
    
    def getListEstimateDateByDate(self, date):
        return FechaEstimada.objects.filter(fecha=date)
        
class QueryStatusProjectInCourse():
    def getListProjectByItem(self, item):
        return EstadoProyectoEnCurso.objects.filter(hito=item, proyecto__estado="C")
    
    def getListProjectByItemAndUser(self, item, user):
        return EstadoProyectoEnCurso.objects.filter(hito=item, proyecto__tutor=user, proyecto__estado="C")
    
    def getProjectByProject(self, project):
        try:
            return EstadoProyectoEnCurso.objects.get(proyecto=project)
        except EstadoProyectoEnCurso.DoesNotExist:
            return None
    def isCompleted(self, status):
        if status :
            return QueryForm().isAllFormsCompletedOfProjectItem(status.proyecto, status.hito)
        else:
            return None
    
class QueryProjectUnresolvedInCourse():
    def getProjectUnresolvedByProject(self, project):
        try:
            return ProyectoParaRevisionEnCurso.objects.get(proyecto=project)
        except:
            return None