from django.forms import ModelForm

from models import Hito, Evaluacion, Pregunta

from queries import QueryEvaluationSystem, QueryItem, QueryEvaluation, QueryQuestion
from proyecto.controllers import cambiaEstadoTodosLosProyectos

class ItemForm(ModelForm):
    class Meta():
        model = Hito
        exclude = ('sistemaEvaluacion', 'orden')

class EvaluationForm(ModelForm):
    class Meta():
        model = Evaluacion
        exclude = ('hito')

class QuestionForm(ModelForm):
    class Meta():
        model = Pregunta
        exclude = ('evaluacion')

class campoForm():
    def __init__(self, request, action, field, item, evaluation, question):
        self.request, self.action, self.field = request, action, field
        self.item,self.evaluation, self.question = Hito(), Evaluacion(), Pregunta()
        self.itemId, self.evaluationId, self.questionId = item, evaluation, question
        
        self.defineForm()

    def datosIniciales(self):
        self.item = QueryItem().getItemByItem(self.itemId)
        data = {}
        if (self.field == "hito"):
            data = {"nombre": self.item.nombre,
                     "plazo": self.item.plazo
            }
        elif (self.field == "evaluacion"):
            self.evaluation = QueryEvaluation().getEvaluationByEvaluation(self.evaluationId)
            data = {"nombre": self.evaluation.nombre,
                     "evaluador": self.evaluation.evaluador,
                     "porcentaje": self.evaluation.porcentaje
            }
        elif (self.field == "pregunta"):
            self.question = QueryQuestion().getQuestionByQuestion(self.questionId)
            data = {"pregunta": self.question.pregunta,
                     "tipoRespuesta": self.question.tipoRespuesta
            }
        
        return data
    
    def defineForm(self):
        forms = {"hito": ItemForm, "evaluacion": EvaluationForm, "pregunta": QuestionForm}
        instance = {"hito": self.item, "evaluacion": self.evaluation, "pregunta": self.question}
        form = forms[self.field]
        if self.request.method == "POST":
            if self.is_delete() :
                self.form = self.DeleteForm()
            else:
                self.form = form(self.request.POST, instance=instance[self.field])
        else :
            if (self.action == "nuevo"):
                self.form = form()
            else:
                initial = self.datosIniciales()
                self.form = form(initial=initial)

    def getForm(self):
        return self.form

    def is_valid(self):
        return self.form.is_valid()
        
    def save(self):
        formProcessData = CampoFormProcessData(self)
        formProcessData.save()
    
    def is_delete(self):
        response = False
        if self.request.method == "POST":
            response =  self.request.POST.get('boton') == "Eliminar"

        return response
    
    class DeleteForm():
        def is_valid(self):
            return True
            
class CampoFormProcessData():
    def __init__(self, form):
        self.form = form
        
    def save(self):
        if self.form.is_delete() :
            self.delete()
        elif self.form.action == "nuevo":
            self.create()
        else:
            self.edit()    
    
    def create(self):
        creation = {"hito": self.createItem, 
                    "evaluacion": self.createEvaluation, 
                    "pregunta": self.createQuestion}
        
        creation[self.form.field]()
        
    def edit(self):
        editation = {"hito": self.editItem, 
                    "evaluacion": self.editEvaluation, 
                    "pregunta": self.editQuestion}
        editation[self.form.field]()
    
    def delete(self):
        deletation = {"hito": self.deleteItem, 
                    "evaluacion": self.deleteEvaluation, 
                    "pregunta": self.deleteQuestion} 
        deletation[self.form.field]()
    
    def createItem(self):
        self.form.item.sistemaEvaluacion = QueryEvaluationSystem().getEvaluationSystemByCourseSelected(self.form.request)
        self.form.item.orden =  len(QueryItem().getListItemsByEvaluationSystem(self.form.item.sistemaEvaluacion)) + 1
        self.form.item.save()
        
    def editItem(self):
        itemDB = QueryItem().getItemByItem(self.form.itemId)
        itemDB.nombre, itemDB.plazo = self.form.item.nombre, self.form.item.plazo 
        itemDB.save()
    
    def deleteItem(self, itemId=None):
        itemId = itemId if itemId != None else self.form.itemId
        itemDB = QueryItem().getItemByItem(itemId)
        evaluations = QueryEvaluation().getListEvaluationsByItem(itemId)
        for evaluation in evaluations :
            self.deleteEvaluation(evaluation.id)
        itemDB.delete()
    
    def createEvaluation(self):
        item = QueryItem().getItemByItem(self.form.itemId)
        self.form.evaluation.hito = item
        self.form.evaluation.save()
    
    def editEvaluation(self):
        evaluationDB = QueryEvaluation().getEvaluationByEvaluation(self.form.evaluationId)
        evaluationDB.nombre, evaluationDB.evaluador, evaluationDB.porcentaje = self.form.evaluation.nombre, self.form.evaluation.evaluador, self.form.evaluation.porcentaje
        evaluationDB.save()
    
    def deleteEvaluation(self, evaluationId=None ):
        evaluationId = evaluationId if evaluationId != None else self.form.evaluationId
        evaluationDB = QueryEvaluation().getEvaluationByEvaluation(evaluationId)    
        questions = QueryQuestion().getListQuestionsByEvaluation(evaluationDB)
        for question in questions:
            self.deleteQuestion(question.id)
        evaluationDB.delete()
       
    def createQuestion(self):
        evaluation = QueryEvaluation().getEvaluationByEvaluation(self.form.evaluationId)
        self.form.question.evaluacion = evaluation
        self.form.question.save()
        
    def editQuestion(self):
        questionDB = QueryQuestion().getQuestionByQuestion(self.form.questionId)
        questionDB.pregunta, questionDB.tipoRespuesta = self.form.question.pregunta, self.form.question.tipoRespuesta
        questionDB.save()
    
    def deleteQuestion(self, questionId=None):
        questionId = questionId if questionId!= None else self.form.questionId
        questionDB = QueryQuestion().getQuestionByQuestion(questionId)
        questionDB.delete()

class EvaluationSystemForm():
    def __init__(self, request):
        self.evaluationSystem = QueryEvaluationSystem().getEvaluationSystemByCourseSelected(request)
        
    def is_valid(self):
        items = QueryItem().getListItemsByEvaluationSystem(self.evaluationSystem)
        total = 0.0
        for item in items:
            evaluations = QueryEvaluation().getListEvaluationsByItem(item)
            for evaluation in evaluations:
                total += evaluation.getPercentage()
        
        if abs(total-100)<0.01 :
            self.errors = None
            return True
        else:
            self.errors = "Els percentatges de les evaluacions han de sumar el 100%."
            return False
    
    def save(self):
        self.evaluationSystem.estado = "A"
        self.evaluationSystem.save()
        cambiaEstadoTodosLosProyectos(self.evaluationSystem.curso)