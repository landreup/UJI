# -*- encoding: utf-8 -*-
from proyecto.models import Proyecto, EstadoProyectoEnCurso,\
    ProyectoParaRevisionEnCurso
from usuario.controllers import usuarioActivo, nombreTutor
from evaluacion.queries import QueryEvaluationSystem, QueryItem
from proyecto.queries import QueryStatusProjectInCourse, QueryProject, QueryEstimateDate,\
    QueryProjectUnresolvedInCourse, QueryJudgeMembers
from usuario.queries import QueryUser
from curso.queries import QueryCourse
from valoracion.controllers import activaFormulario

def vistaCoordinador(request):
    if ("coordinacio" in request.path) : return True
    else : return False

def vistaProfesor(request):
    if ("professorat" in request.path) : return True
    else : return False

def listaProyectosPendientes(request):
    return QueryProject().getListProjectByCourseSelectedStatus(request, "P")

def listaProyectosFinalizados(request):
    return QueryProject().getListProjectByCourseSelectedStatus(request, "F")

def gruposProyectosEnCurso(request, profesorid):
    groups = []
    evaluationSystem = QueryEvaluationSystem().getEvaluationSystemByCourseSelected(request)
    #"Por Asignar"
    lockProjects = listaProyectosPorRolStatus(request, profesorid, "L")
    if lockProjects : groups.append({'campo': "Projectes pendents de revisió", 'lista': lockProjects})
    
    "Por hitos"
    for item in QueryItem().getListItemsByEvaluationSystem(evaluationSystem):
        lista = listaProyectosPorRolYItem(request, profesorid, item)
        if lista:
            groups.append({'campo': "Projectes en " + item.nombre.lower(), 'lista': lista})
    
    return groups

def listaProyectosPorRolStatus(request, profesorUserUJI, status):
    lista = []
    user = QueryUser().getUserByUserUJI(profesorUserUJI)
    
    if vistaCoordinador(request):
        if user : 
            listaQuery = QueryProject().getListProjectByCourseSelectedStatusTutor(request, status, user)
        else :
            listaQuery = QueryProject().getListProjectByCourseSelectedStatus(request, status)
    elif vistaProfesor(request):
        #USUARIO ACTIVO !!!!!
        
        listaQuery = QueryProject().getListProjectByCourseSelectedStatus(request, status)
    
    if status =="L" or status =="C":
        for elem in listaQuery:
            date =  "No disponible"
            lista.append({'proyecto': elem, 'fecha': date})
    else:
        lista = listaQuery
    return lista

def listaProyectosPorRolYItem(request, profesorUserUJI, item):
    lista = []
    
    user = QueryUser().getUserByUserUJI(profesorUserUJI)
        
    if vistaCoordinador(request):
        if user :
            listaQuery = QueryStatusProjectInCourse().getListProjectByItemUser(item, user)
        else: 
            listaQuery = QueryStatusProjectInCourse().getListProjectByItem(item)
    elif vistaProfesor(request):
        #USUARIO ACTIVO !!!!!
        
        listaQuery = QueryStatusProjectInCourse().getListProjectByItem(item)
    
    
    for elem in listaQuery:
        estimateDate = QueryEstimateDate().getEstimateDateByProjectAndItem(elem.proyecto, item)
        date =  estimateDate.fecha.strftime("%d/%m/%Y") if estimateDate else "No disponible"
        lista.append({'proyecto': elem.proyecto, 'fecha': date})
    return lista
    
def tituloListadoProyectos(request, profesorid):
    if vistaProfesor(request):
        titulo = "Projectes Assignats"
    elif vistaCoordinador(request):
        if profesorid :
            titulo = "Projectes que tutoritza " + nombreTutor(profesorid)
        else:
            titulo = "Gestió de Projectes"
            
    return titulo

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
