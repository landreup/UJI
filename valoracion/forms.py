from django import forms

from models import Valoracion, EvaluacionesFormulario, Formulario
from queries import QueryEvaluationForm

from alumno.controllers import alumnoPorId
from curso.controllers import cursoSeleccionado
from evaluacion.queries import QueryEvaluation, QueryQuestion
from proyecto.queries import QueryProject

import random, base64

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
        
    def strResponseType(self, field, responseType):
        if responseType == "A" :
            return "<select id=\"id_"+ field +"\" name=\""+ field +"\"><option value=\"1\" selected=\"selected\">No Apte</option><option value=\"5\">Apte</option></select>"  
        elif responseType == "I":
            return "<input id=\"id_"+ field + "\" name=\"" + field + "\" type=\"radio\" value=\"1\"/>" + \
                   "<input id=\"id_"+ field + "\" name=\"" + field + "\" type=\"radio\" value=\"2\"/>" + \
                   "<input id=\"id_"+ field + "\" name=\"" + field + "\" type=\"radio\" value=\"3\"/>" + \
                   "<input id=\"id_"+ field + "\" name=\"" + field + "\" type=\"radio\" value=\"4\"/>" + \
                   "<input id=\"id_"+ field + "\" name=\"" + field + "\" type=\"radio\" value=\"5\"/>"
        else:
            return ""
        
    def fieldName(self, evaluation, question):
        return "evaluacionFormulario" + str(evaluation.id) + "_pregunta" + str(question.id)
        
    def __str__(self):
        #return str(len(self.questions))
        htmlForm = ""
        for question in self.questions :
            field = self.fieldName(self.evaluation, question)
            htmlForm += "<label for=\"id_"+ field + "\">" + question.pregunta + "</label>" + self.strResponseType(field, question.tipoRespuesta) + "<br/>"
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

class EvaluationFormForm():
    def __init__(self, request, form):
        self.evaluations=[]
        for evaluationForm in QueryEvaluationForm().getListEvaluationFormByForm(form):
            self.evaluations.append(self.EvaluationFormComplete(request, evaluationForm))
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
        
    class EvaluationFormComplete():
        def __init__(self, request, evaluationForm):
            self.evaluation = evaluationForm.evaluacion
            self.valorationForm = ValorationForm(request, evaluationForm)

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
        course = cursoSeleccionado(self.request)
        student = alumnoPorId(self.studentUser)
        project = QueryProject().getProjectByCourseAndStudent(course, student)
        for rol in QueryEvaluation().getRoles().keys():
            evaluationsItemRol = QueryEvaluation().getListEvaluationsByItemAndRol(self.item, rol)
            if evaluationsItemRol :
                email = QueryProject().getEmailByProjectAndEvaluator(project, rol)
                form = Formulario()
                form.proyecto = project
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