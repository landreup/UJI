# -*- encoding: utf-8 -*-
from proyecto.models import Proyecto, EstadoProyectoEnCurso,\
    ProyectoParaRevisionEnCurso
from evaluacion.queries import QueryEvaluationSystem, QueryItem
from proyecto.queries import QueryStatusProjectInCourse, QueryProject, QueryEstimateDate,\
    QueryProjectUnresolvedInCourse, QueryJudgeMembers
from curso.queries import QueryCourse
from valoracion.controllers import activaFormulario
from django.core.mail.message import EmailMessage
from settings import SERVER_NAME

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
    return porRellenar

def tribunalPorRellenarProyecto(proyecto, item):
    if QueryItem().hasTribunalEvaluationThisItem(item):
        if QueryJudgeMembers().isJudgeDefinedForProject(proyecto):
            return False
        else:
            return True
    else:
        return False

def eliminaProyectoPorRellenar(proyecto):
    proyectoPendiente = QueryProjectUnresolvedInCourse().getProjectUnresolvedByProject(proyecto)
    if proyectoPendiente : proyectoPendiente.delete()

def emailAvisoProyectoEnRevision(project, item, warningCoordinators):
    body = "" 
    body += u"El projecte de l'alumne " + project.alumno.nombreCompleto() + u" necesita una revisió de la teva part per activar " + unicode(item).lower() + ".\n"
    body += "\n"
    body += u"Per favor, accedeix a l'administració del projecte y introduiex les dades necessàries.\n"
    body += "http://" + SERVER_NAME + "/professorat/projectes/" + project.alumno.usuarioUJI + "/edita/" + ' \n'
    body += "-------------------------------\n"
    body += "Para: "
    body += "Tutor " + project.tutor.getMail() if not warningCoordinators else "Coordinadores" 
    email = EmailMessage()
    email.subject = u"Necesitat d'intervenció en el projecte de l'alumne " + unicode(project.alumno.nombreCompleto())+ " per activar" +  unicode(item).lower()
    email.from_email = 'UJI - Evaluació d\'estudiants de projecte Fi de Grau<provauji@gmail.com>'
    email.to = ['landreup@gmail.com', 'aramburu@uji.es', 'lopeza@uji.es']
    email.body = body
    email.send()
    
def buildErrors(textProjectIncomplete, isTribunalIncomplete, dateEstimateNextItem, item):
    errors = ""
    if textProjectIncomplete :
        errors += textProjectIncomplete
    
    if isTribunalIncomplete:
        separator = "|" if errors else ""
        errors += separator + "tribunal"
        
    if not dateEstimateNextItem:
        separator = "|" if errors else ""
        errors += separator + "id_" + str(item.id) + "-fecha"
    
    return errors
    
def cambiaEstadoProyecto(proyecto, cambiaPendiente=False):
    if proyecto.estado =="L" or proyecto.estado=="C" or cambiaPendiente:
        status = QueryStatusProjectInCourse().getProjectByProject(proyecto)
        
        if (QueryStatusProjectInCourse().isCompleted(status) and status) or not status :
        
            nextItem = QueryItem().getNextItem(status.hito) if status else QueryItem().getFirstItemCourse(proyecto.curso)
        
            textProjectIncomplete = camposPorRellenarProyecto(proyecto, nextItem)
            
            isProjectIncomplete = False if textProjectIncomplete == "" else True
            
            isTribunalIncomplete = tribunalPorRellenarProyecto(proyecto, nextItem)
            
            dateEstimateNextItem = QueryEstimateDate().getEstimateDateByProjectAndItem(proyecto, nextItem) if nextItem else True
            
            evaluationSystem = QueryEvaluationSystem().getEvaluationSystemByCourse(proyecto.curso)
            
            if not isProjectIncomplete and not isTribunalIncomplete and dateEstimateNextItem and evaluationSystem.estado=="A":
                revision = QueryProjectUnresolvedInCourse().getProjectUnresolvedByProject(proyecto)
                if revision : revision.delete()
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
                revision = QueryProjectUnresolvedInCourse().getProjectUnresolvedByProject(proyecto)
                if revision : revision.delete()
                else :
                    emailAvisoProyectoEnRevision(proyecto, nextItem, isTribunalIncomplete)
                
                textProjectIncomplete = buildErrors(textProjectIncomplete, isTribunalIncomplete, dateEstimateNextItem, nextItem)
                                
                pendentStatus = ProyectoParaRevisionEnCurso()
                pendentStatus.proyecto = proyecto
                pendentStatus.campos = textProjectIncomplete
                pendentStatus.save()
                proyecto.estado = "L"
                proyecto.save()

def cambiaEstadoTodosLosProyectos(curso):
    listProjects = QueryProject().getListProjectByCourseAndStatus(curso, "L")
    for project in listProjects:
        cambiaEstadoProyecto(project)

def getlabelsFields(course):
    labels = {}
    labels['id_proyecto-inicio'] = u"data d\'inici"
    labels['id_proyecto-dedicacionSemanal'] = u"dedicació semanal"
    labels['tribunal'] = 'tribunal'
    for item in QueryItem().getListItemsByEvaluationSystem(QueryEvaluationSystem().getEvaluationSystemByCourse(course)):
        key = 'id_' + str(item.id) + '-fecha'
        labels[key] = 'data estimada de ' + unicode(item)
    return labels

def mensajeError(revision):
    fields = revision.campos
    course = revision.proyecto.curso
    listFields = fields.split('|')
    errors = ""
    labelsFields = getlabelsFields(course)
    if len(listFields) > 1:
        errors = "Per favor, ompli els camps "
        i = 0
        for field in listFields:
            errors += labelsFields[field]
            i += 1
            errors += ", " if  i != len(listFields) else "."  
    elif len(listFields) == 1 :
        errors = "Per favor, ompli " + labelsFields[listFields[0]] + "."
    return errors
    