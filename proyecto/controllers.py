# -*- encoding: utf-8 -*-
from proyecto.models import Proyecto, EstadoProyectoEnCurso,\
    ProyectoParaRevisionEnCurso
from usuario.controllers import nombreTutor
from evaluacion.queries import QueryEvaluationSystem, QueryItem
from proyecto.queries import QueryStatusProjectInCourse, QueryProject, QueryEstimateDate,\
    QueryProjectUnresolvedInCourse, QueryJudgeMembers
from usuario.queries import QueryUser
from curso.queries import QueryCourse
from valoracion.controllers import activaFormulario

def isEditable(course):
    return QueryCourse().isActual(course) and QueryEvaluationSystem().isEvaluationSystemEnabledByCourse(course)

class ProjectInCourse:
    def __init__(self, project, date):
        self.proyecto = project
        self.fecha = date

class GroupElement:
    def __init__(self, listProject, campo):
        self.campo = campo
        self.lista = listProject
        
class LockGroupElement(GroupElement):
    def __init__(self, listProject):
        self.campo = "Projectes pendents de revisió"
        self.lista = []
        for element in listProject:
            self.lista.append(ProjectInCourse(element, "No Disponible"))
            
class InCourseGroupElement(GroupElement):
    def __init__(self, listProject, item):
        self.campo = "Projectes en " + item.nombre.lower()
        self.lista = []
        for element in listProject:
            estimateDate = QueryEstimateDate().getEstimateDateByProjectAndItem(element.proyecto, item)
            date =  estimateDate.fecha.strftime("%d/%m/%Y") if estimateDate else "No disponible"
            self.lista.append({'proyecto': element.proyecto, 'fecha': date})

def gruposProyectosEnCursoTodos(course):
    groups = []
    evaluationSystem = QueryEvaluationSystem().getEvaluationSystemByCourse(course) 
    lockProjects = QueryProject().getListProjectByCourseAndStatus(course, "L")
    if lockProjects : groups.append(LockGroupElement(lockProjects))
   
    for item in QueryItem().getListItemsByEvaluationSystem(evaluationSystem):
        lista = QueryStatusProjectInCourse().getListProjectByItem(item)
        if lista : groups.append(InCourseGroupElement(lista, item)) 
    return groups

def gruposProyectosEnCursoProfesor(course, user):
    groups = []
    evaluationSystem = QueryEvaluationSystem().getEvaluationSystemByCourse(course)
    lockProjects = QueryProject().getListProjectByCourseStatusTutor(course, "L", user)
    if lockProjects : groups.append(LockGroupElement(lockProjects))
    
    for item in QueryItem().getListItemsByEvaluationSystem(evaluationSystem):
        lista = QueryStatusProjectInCourse().getListProjectByItemAndUser(item, user)
        if lista : groups.append(InCourseGroupElement(lista, item))
    
    return groups

def copiaProyectosEnCursoCursoActualAProyectosPendientesCursoNuevo(course):
    beforeCourse = QueryCourse().getCourseBefore(course)
    projects = QueryProject().getListProjectInCourseByCourse(beforeCourse)
    for project in projects :
        newProject = Proyecto()
        newProject.alumno = project.alumno
        newProject.tutor = project.tutor
        newProject.supervisor = project.supervisor
        newProject.email = project.email
        newProject.curso = course
        newProject.empresa = project.empresa
        newProject.telefono = project.telefono
        newProject.titulo = project.titulo
        newProject.inicio = project.inicio
        newProject.dedicacionSemanal = project.dedicacionSemanal
        newProject.otrosDatos = project.otrosDatos
        newProject.estado = "P"
        newProject.save()

def camposPorRellenarProyecto(proyecto, item):
    porRellenar = ""
    if not proyecto.inicio :
        porRellenar = "id_proyecto-inicio"
    if not proyecto.dedicacionSemanal :
        separador = "|" if porRellenar else ""
        porRellenar += separador + "id_proyecto-dedicacionSemanal"
        
    if QueryItem().hasTribunalEvaluationThisItem(item):
        if not QueryJudgeMembers().isJudgeDefinedForProject(proyecto):
            separador = "|" if porRellenar else ""
            porRellenar += separador + "tribunal"
    
    return porRellenar

def eliminaProyectoPorRellenar(proyecto):
    proyectoPendiente = QueryProjectUnresolvedInCourse().getProjectUnresolvedByProject(proyecto)
    if proyectoPendiente : proyectoPendiente.delete()

def cambiaEstadoProyecto(proyecto, cambiaPendiente=False):
    
    if proyecto.estado =="L" or proyecto.estado=="C" or cambiaPendiente:
        status = QueryStatusProjectInCourse().getProjectByProject(proyecto)
        
        if (QueryStatusProjectInCourse().isCompleted(status) and status) or not status :
        
            nextItem = QueryItem().getNextItem(status.hito) if status else QueryItem().getFirstItemCourse(proyecto.curso)
        
            textProjectIncomplete = camposPorRellenarProyecto(proyecto, nextItem)
            
            isProjectIncomplete = False if textProjectIncomplete == "" else True
            
            dateEstimateNextItem = QueryEstimateDate().getEstimateDateByProjectAndItem(proyecto, nextItem) if nextItem else True
            
            evaluationSystem = QueryEvaluationSystem().getEvaluationSystemByCourse(proyecto.curso)
            
            if not isProjectIncomplete and dateEstimateNextItem and evaluationSystem.estado=="A":
                if status : status.delete()
                if nextItem:
                    status = EstadoProyectoEnCurso()
                    status.proyecto = proyecto
                    status.hito = nextItem
                    status.save()
                    activaFormulario(proyecto, nextItem)
                proyecto.estado="C" if nextItem else "F"
                proyecto.save()
                eliminaProyectoPorRellenar(proyecto)
            else:
                pendentStatus = ProyectoParaRevisionEnCurso()
                pendentStatus.proyecto = proyecto
                if not dateEstimateNextItem:
                    if isProjectIncomplete:
                        textProjectIncomplete += "|id_"+ str(nextItem.id) + "-fecha"
                    else: 
                        textProjectIncomplete = "id_"+  str(nextItem.id) + "-fecha"
                
                if isProjectIncomplete : 
                    textProjectIncomplete += "|Desactivado" if evaluationSystem.estado=="D" else ""
                else : 
                    textProjectIncomplete = "Desactivado" if evaluationSystem.estado=="D" else ""
                  
                pendentStatus.campos = textProjectIncomplete
                pendentStatus.save()
                proyecto.estado = "L"
                proyecto.save()

def cambiaEstadoTodosLosProyectos(curso):
    listProjects = QueryProject().getListProjectByCourseAndStatus(curso, "L")
    for project in listProjects:
        cambiaEstadoProyecto(project)
