# -*- encoding: utf-8 -*-
from django import forms
from models import Valoracion, EvaluacionesFormulario, Formulario
from queries import QueryEvaluationForm

from alumno.controllers import alumnoPorId
from curso.queries import QueryCourse
from evaluacion.queries import QueryEvaluation, QueryQuestion, QueryItem
from proyecto.queries import QueryProject

import random, base64
from proyecto.controllers import cambiaEstadoProyecto
from valoracion.queries import QueryForm
import datetime
import time

class ValorationForm():
    def __init__(self, request, evaluationForm):
        self.questions = QueryQuestion().getListQuestionsByEvaluation(evaluationForm.evaluacion)
        self.evaluation = evaluationForm.evaluacion
        self.evaluationForm = evaluationForm
        self.valorations = []

        if request.method == 'POST' :
            for question in self.questions :
                field = self.fieldName(self.evaluation, question)
                if request.POST.get(field, '') :
                    response = self.Response(question, int(request.POST.get(field, '')))
                    self.valorations.append(response)
        
    def unicodeResponseType(self, field, responseType):
        if responseType == "A" :
            return u"<select id=\"id_"+ field +"\" name=\""+ field +"\"><option value=\"1\" selected=\"selected\">No Apte</option><option value=\"5\">Apte</option></select>"  
        elif responseType == "I":
            return u"<input id=\"id_"+ field + "\" name=\"" + field + "\" type=\"radio\" value=\"1\"/>" + \
                   u"<input id=\"id_"+ field + "\" name=\"" + field + "\" type=\"radio\" value=\"2\"/>" + \
                   u"<input id=\"id_"+ field + "\" name=\"" + field + "\" type=\"radio\" value=\"3\"/>" + \
                   u"<input id=\"id_"+ field + "\" name=\"" + field + "\" type=\"radio\" value=\"4\"/>" + \
                   u"<input id=\"id_"+ field + "\" name=\"" + field + "\" type=\"radio\" value=\"5\"/>"
        else:
            return ""
        
    def fieldName(self, evaluation, question):
        return u"evaluacionFormulario" + str(evaluation.id) + u"_pregunta" + str(question.id)
        
    def __unicode__(self):
        #return str(len(self.questions))
        htmlForm = ""
        for question in self.questions :
            field = self.fieldName(self.evaluation, question)
            htmlForm += u"<label for=\"id_"+ field + "\">" + unicode(question.pregunta) + u"</label>" + self.unicodeResponseType(field, question.tipoRespuesta) + u"<br/>"
        return htmlForm
    
    def isValorationValid(self, response):
        if (response.question.tipoRespuesta == "A") :
            return response.valoration == 1 or response.valoration == 5 
        elif (response.question.tipoRespuesta == "I"):
            return response.valoration > 0 and response.valoration < 6
        else:
            return False
    
    def is_valid(self):
        if (len(self.questions) != len(self.valorations)) :
            self.errors = "Hi han questions sense respondre." 
            return False
        
        isAllCorrect = True
        for valoration in self.valorations :
            if not self.isValorationValid(valoration):
                isAllCorrect = False
                self.errors = "Hi ha alguna resposta que no es correcta"
                break
        
        return isAllCorrect
    
    def save(self):
        for valoration in self.valorations:
            newValoration = Valoracion()
            newValoration.pregunta = valoration.question
            newValoration.evaluacionFormulario = self.evaluationForm
            newValoration.respuesta = valoration.valoration
            newValoration.save()
    
    class Response():
        def __init__(self, question, valoration):
            self.question = question
            self.valoration = valoration
            
class EvaluationForm():
    def __init__(self, request, evaluationForm):
        self.evaluation = evaluationForm.evaluacion
        self.evaluationForm = evaluationForm
        
        self.response = ""
        self.errors = ""
        if request.method == 'POST' :
            field = self.fieldName()
            if request.POST.get(field, '') :
                self.response = request.POST.get(field, '') 
    
    def fieldName(self):
        return u"evaluacionFormulario" + str(self.evaluation.id)
    
    def __unicode__(self):
        field = self.fieldName()
        value = self.response #if self.response else ""
        response = u"<label for=\"id_"+ field + u"\">Qualificació</label>"
        response += u"<input id=\"id_"+ field + "\" name=\"" + field + "\" type=\"text\" value=\"" + value + "\"/>"
        response += self.errors
        return response
    
    def is_valid(self):
        try:
            self.response = float(self.response)
            return True
        except ValueError: 
            self.errors = u"No has introduit un número válid"
            return False
        
    def save(self):
        self.evaluationForm.valoracionEvaluacion = self.response
        self.evaluationForm.save()

class EvaluationFormForm():
    def __init__(self, request, form):
        self.form = form
        self.evaluations=[]
        unresolved =  form.isUnresolved()
        for evaluationForm in QueryEvaluationForm().getListEvaluationFormByForm(form):
            self.evaluations.append(self.EvaluationFormComplete(request, evaluationForm, not unresolved))
        self.evaluaciones = self.evaluations
    
    def is_valid(self):
        isAllCorrect = True
        for evaluation in self.evaluations :
            if not evaluation.valorationForm.is_valid() :
                isAllCorrect = False
                break
        return isAllCorrect
        
    def save(self):
        for evaluation in self.evaluations :
            evaluation.valorationForm.save()
        self.form.fechaValorado = datetime.date.today()
        self.form.save()
        if QueryForm().isAllFormsCompletedOfProjectItem(self.form.proyecto, self.form.hito):
            self.form.fechaBloqueado = datetime.date.today()
            self.form.save()
            cambiaEstadoProyecto(self.form.proyecto)
        
    class EvaluationFormComplete():
        def __init__(self, request, evaluationForm, questions=True):
            self.evaluation = evaluationForm.evaluacion
            self.valorationForm = ValorationForm(request, evaluationForm) if questions else EvaluationForm(request, evaluationForm)
    
class FormForm():
    class DateField():
        def __str__(self):
            return "<input type=\"text\" id=\"dateAppreciated\" name=\"date\" class=\"date\"/>"
                        
    dateAppreciated = DateField()
    def __init__(self, request, alumnoId, itemId):
        self.request = request
        self.studentUser = alumnoId
        self.item = itemId
        if self.request.method == "POST" :
            self.dateAppreciated = self.request.POST.get('date', '')

    def is_valid(self):
        return True

    def save(self):
        course = QueryCourse().getCourseSelected(self.request)
        student = alumnoPorId(self.studentUser)
        project = QueryProject().getProjectByCourseAndStudent(course, student)
        for rol in QueryEvaluation().getRoles().keys():
            evaluationsItemRol = QueryEvaluation().getListEvaluationsByItemAndRol(self.item, rol)
            if evaluationsItemRol :
                email = QueryProject().getEmailByProjectAndEvaluator(project, rol)
                form = Formulario()
                form.proyecto = project
                item = QueryItem().getItemByItem(self.item)
                form.hito = item
                form.rol = rol
                form.fechaEstimada = self.dateAppreciated
                form.email = email
                form.codigo = self.aleatoryString()
                form.save()
                for evaluation in evaluationsItemRol:
                    evaluationForm = EvaluacionesFormulario()
                    evaluationForm.formulario = form
                    evaluationForm.evaluacion = evaluation
                    evaluationForm.save()
                
    def aleatoryString(self):
        nbits = 100 * 6 + 1
        bits = random.getrandbits(nbits)
        uc = u"%0x" % bits
        newlen = (len(uc) / 2) * 2 # we have to make the string an even length
        ba = bytearray.fromhex(uc[:newlen])
        return base64.urlsafe_b64encode(str(ba))[:100]