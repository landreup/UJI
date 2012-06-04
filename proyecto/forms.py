# -*- encoding: utf-8 -*-

from django.forms import ModelForm

from models import Proyecto, MiembroTribunal, FechaEstimada
from queries import QueryProject, QueryJudgeMembers, QueryEstimateDate

from alumno.models import Alumno

from alumno.forms import AlumnoForm

from evaluacion.queries import QueryEvaluationSystem, QueryItem
from usuario.queries import QueryUser
from curso.queries import QueryCourse

from datetime import datetime
from proyecto.controllers import cambiaEstadoProyecto
from proyecto.queries import QueryStatusProjectInCourse
from alumno.queries import QueryStudent

class ProyectoForm(ModelForm):
    class Meta():
        model = Proyecto
        exclude = ('curso', 'alumno', 'estado', 'tutor')

class TutorForm(ModelForm):
    class Meta():
        model = Proyecto
        include = ('tutor')

class EstimateDateForm(ModelForm):
    class Meta():
        model = FechaEstimada
        exclude = ('hito', 'proyecto')
    
class EstimateDateItemForm():
    def __init__(self, request, studentUserUJI):
        self.request = request
        items = QueryItem().getListItemsByEvaluationSystem(QueryEvaluationSystem().getEvaluationSystemByCourseSelected(request))
        
        self.project = None 
        if studentUserUJI : self.project = QueryProject().getProjectByCourseAndStudent(QueryCourse().getCourseSelected(request), QueryStudent().getStudentByUserUJI(studentUserUJI))       
        
        projectStatus = QueryStatusProjectInCourse().getProjectByProject(self.project)
        if projectStatus :
            nextItem = QueryItem().getNextItem(projectStatus.hito)
        else :
            nextItem = QueryItem().getFirstItemCourse(self.project.curso)
        self.forms = []
        self.fechas = []
        inputDate = False
        for item in items :
            if self.project.estado == "C" :
                if item == projectStatus.hito : inputDate = True
            elif self.project.estado == "L" :
                if item == nextItem : inputDate = True
            if inputDate :
                if request.method == "POST" :
                    fecha = request.POST.get(str(item.id)+"-fecha", '')
                    form = {"id": "id_" + str(item.id)+"-fecha", "label": item.nombre, "form": EstimateDateForm(request.POST, prefix=str(item.id))}
                    if fecha: self.fechas.append({"item": item, "fecha": fecha})
                else:
                    form = {"id": "id_" + str(item.id)+"-fecha", "label": item.nombre, "form": EstimateDateForm(prefix=str(item.id))}
                    estimateDate = QueryEstimateDate().getEstimateDateByProjectAndItem(self.project, item)
                    if estimateDate :
                        form["form"].initial["fecha"] = estimateDate.fecha
                self.forms.append(form)
    
    def is_valid(self):
        isValid = True
        for fecha in self.fechas:
            for form in self.forms:
                fecha_id = "id_" + str(fecha["item"].id) + "-fecha"
                if form["id"] == fecha_id :
                    isValid = isValid and form['form'].is_valid()
                    
        return isValid
    
    def save(self, project):
        for fecha in self.fechas:
            fechaDB = QueryEstimateDate().getEstimateDateByProjectAndItem(project, fecha["item"])
            if not fechaDB : fechaDB = FechaEstimada()
            fechaDB.proyecto = project
            fechaDB.hito = fecha["item"]
            d = datetime.strptime(fecha["fecha"], '%d/%m/%Y')
            date_string = d.strftime('%Y-%m-%d')
            fechaDB.fecha = date_string 
            fechaDB.save()

class MemberJudgeForm(ModelForm):
    class Meta():
        model = MiembroTribunal
        exclude = ('idMiembro', 'proyecto')

class TribunalForm():
    def __init__(self, request, studentUserUJI):
        self.numberOfJudgeMembers = 3
        
        self.request = request
        
        self.project, self.judgeMembers = None, None
        
        if studentUserUJI : 
            self.project = QueryProject().getProjectByCourseAndStudent(QueryCourse().getCourseSelected(self.request), QueryStudent().getStudentByUserUJI(studentUserUJI))
            self.judgeMembers = QueryJudgeMembers().getListMembersByProject(self.project)
        
        self.forms = []
        self.id_members = []
        for i in xrange(self.numberOfJudgeMembers) :
            if request.method == 'POST':
                id_member = request.POST.get("miembro"+str(i)+"-miembro", '')
                form = MemberJudgeForm(request.POST, prefix="miembro"+str(i))
                if id_member : self.id_members.append({'id': i+1, 'id_member': id_member})
            else:
                form = MemberJudgeForm(prefix="miembro"+str(i))
                form.fields["miembro"].queryset = QueryUser().getListOfUser()
                if self.judgeMembers: form.initial["miembro"] = self.judgeMembers[i].miembro
            self.forms.append(form)
            
    def is_valid(self):
        repeat = False
        for i in xrange(len(self.id_members)):
            for j in xrange(i+1, len(self.id_members)):
                if self.id_members[i] == self.id_members[j] : repeat = True
            
        if repeat :
            self.errors = "Se han repetido miembros del tribunal"
            return False
        
        return True
    
    def save(self, project):
        if not self.project : self.project = QueryProject().getProjectByCourseAndStudent(QueryCourse().getCourseSelected(self.request), self.student)
        self.judgeMembers = QueryJudgeMembers().getListMembersByProject(project)
        for member in self.id_members:
            user = QueryUser().getUserById(member['id_member'])
            memberDB = MiembroTribunal()
            if self.judgeMembers: 
                for judgeMember in self.judgeMembers:
                    if judgeMember.idMiembro == member['id'] :
                        memberDB = judgeMember
            memberDB.proyecto = project
            memberDB.idMiembro = member['id']
            memberDB.miembro = user
            memberDB.save()

    def __unicode__(self):
        response = u""
        for form in self.forms :
            response += form.as_p()
        return response

class ProyectoAlumnoForm():
    def __init__(self, request, action="nuevo", alumnoUserUJI="", tutor=None):
        self.alumno = Alumno()
        self.proyecto = Proyecto()
        self.tutor = None
        self.action = action
        self.request = request
        self.alumnoid = alumnoUserUJI
        self.pendiente = None
        
        self.tutorForm = None
        self.tribunalForm = None
        self.dateForm = None
        
        coordinator = tutor == None
        
        if action != "nuevo" :
            self.alumno = QueryStudent().getStudentByUserUJI(alumnoUserUJI)
            self.proyecto = QueryProject().getProjectByCourseAndStudent(QueryCourse().getCourseSelected(self.request), self.alumno)
            
            self.estado = self.proyecto.estado
            if self.proyecto.estado == "L": 
                statusProject = QueryStatusProjectInCourse().getProjectByProject(self.proyecto)
                item = statusProject.hito if statusProject else None
                nextItem = QueryItem().getNextItem(item) if item else QueryItem().getFirstItemCourse(self.proyecto.curso)
                if QueryItem().hasTribunalEvaluationThisItem(nextItem):
                    self.tribunalForm = TribunalForm(request, alumnoUserUJI)            
            self.dateForm = EstimateDateItemForm(request, alumnoUserUJI) if self.estado != "P" else None
        
        self.alumnoForm = AlumnoForm(prefix='alumno', instance=self.alumno)
        self.proyectoForm = ProyectoForm(prefix='proyecto', instance=self.proyecto)
        
        if coordinator :
            if action != "nuevo" :
                self.tutor = self.proyecto.tutor
            self.tutorForm = TutorForm(prefix='tutor')
            self.tutorForm.fields["tutor"].queryset = QueryUser().getListOfTutorCoordinator()
            if tutor:
                self.tutorForm.initial["tutor"] = tutor
        else:
            self.tutor = tutor
        
        if request.method == 'POST': # Leer los datos
            if action != "nuevo":
                if self.estado == "L": 
                    statusProject = QueryStatusProjectInCourse().getProjectByProject(self.proyecto)
                    item = statusProject.hito if statusProject else None
                    nextItem = QueryItem().getNextItem(item) if item else QueryItem().getFirstItemCourse(self.proyecto.curso)
                    
                    if QueryItem().hasTribunalEvaluationThisItem(nextItem):
                        self.tribunalForm = TribunalForm(request, alumnoUserUJI)
                self.dateForm = EstimateDateItemForm(request, alumnoUserUJI) if self.estado != "P" else None
            
            self.alumnoForm = AlumnoForm(request.POST, prefix='alumno', instance=self.alumno)
            self.proyectoForm = ProyectoForm(request.POST, prefix='proyecto', instance=self.proyecto)
            if coordinator :
                self.tutorId = self.proyectoForm.data["tutor-tutor"]
            else:
                self.tutorId = self.tutor.id
                         
    def is_valid(self):
        self.alumnoEsValido = self.alumnoForm.is_valid()
        if ( not self.alumnoEsValido and self.isEditing()):
            if ( self.alumnoForm.data["alumno-usuarioUJI"] == self.alumnoid ):
                self.alumnoEsValido = True

        self.tutor = self.Tutor(self.tutorId)
        tutor = self.tutor
        a = fasdf()
        if self.tutorForm :
            tutorIsValid = self.tutor.is_valid()
        else:
            tutorIsValid = True

        if self.tribunalForm :
            tribunalIsValid = self.tribunalForm.is_valid()
        else:
            tribunalIsValid = True

        if self.dateForm :
            dateIsValid = self.dateForm.is_valid()
        else:
            dateIsValid = True
        
        return (self.alumnoEsValido 
                and self.proyectoForm.is_valid() 
                and tutorIsValid
                and tribunalIsValid
                and dateIsValid
        )
    
    def isEditing(self):
        return self.action == "edita"
    
    def isTutorValid(self, tutorId):
        tutor = self.Tutor(tutorId)
        valid = tutor.is_valid()
        if not valid :
            valid =  tutor.is_empty() and self.isEditing()
        return valid
        
    def getAlumnoProyecto(self):
        return self.alumno, self.proyecto
    
    def getAlumnoId(self):
        return self.alumnoid
    
    def getAccion(self):
        return self.accion
    
    def save(self):
        if (self.action == "nuevo"):
            self.createProjectStudent()
        else : # edicion
            self.editProjectStudent()
        
        
        if self.tribunalForm : 
            self.tribunalForm.save(self.proyecto)
        if self.dateForm : self.dateForm.save(self.proyecto)
        
        cambiaEstadoProyecto(self.proyecto)
    
    def createProjectStudent(self):
        self.createStudent()
        self.createProject()
    
    def createStudent(self):
        self.alumno.save()
    
    def createProject(self):
        self.proyecto.alumno = self.alumno
        self.proyecto.curso = QueryCourse().getCourseSelected(self.request)
        self.proyecto.tutor = self.tutor.user
        self.proyecto.estado = "L"
        self.proyecto.save()

    def editProjectStudent(self):
        self.editStudent()
        self.editProject()
    
    def editStudent(self):
        alumnoDB = QueryStudent().getStudentByUserUJI(self.alumnoid)
        alumnoDB.nombre = self.alumno.nombre
        alumnoDB.usuarioUJI = self.alumno.usuarioUJI
        alumnoDB.save()
        
        self.alumno = alumnoDB
        
    def editProject(self):
        curso = QueryCourse().getCourseSelected(self.request)
     
        alumno = QueryStudent().getStudentByUserUJI(self.alumnoid)
        
        proyectoDB = QueryProject().getProjectByCourseAndStudent(curso, alumno)
        proyectoDB.tutor = self.tutor.user
        proyectoDB.supervisor = self.proyecto.supervisor
        proyectoDB.email = self.proyecto.email
        proyectoDB.empresa = self.proyecto.empresa
        proyectoDB.telefono = self.proyecto.telefono
        proyectoDB.titulo = self.proyecto.titulo
        proyectoDB.inicio = self.proyecto.inicio
        proyectoDB.dedicacionSemanal = self.proyecto.dedicacionSemanal
        proyectoDB.otrosDatos = self.proyecto.otrosDatos
        proyectoDB.estado = self.estado
    
        proyectoDB.save()
        
        self.proyecto = proyectoDB
        
    class Tutor():
        def __init__(self, tutorId):
            self.tutorId = tutorId
            self.user = None
            
        def is_valid(self):
            if (not self.is_empty()) :
                self.user = QueryUser().getUserById(self.tutorId)
                if self.user.isTutor() : return True
                else: return False
            else:
                return False
        
        def is_empty(self):
            return self.tutorId == ''