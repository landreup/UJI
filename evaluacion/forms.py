from django.forms import ModelForm

from models import Hito, Evaluacion, Pregunta

from queries import QueryEvaluationSystem, QueryItem, QueryEvaluation, QueryQuestion

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
    def __init__(self, request, action, field, item, evaluation, question, formAction="crea"):
        self.request, self.action, self.formAction, self.field = request, action, formAction, field
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
                     "miembrosTribunal": self.evaluation.miembrosTribunal
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
        if (self.formAction == "crea"):
            if (self.action == "nuevo"):
                self.form = form()
            else:
                initial = self.datosIniciales()
                self.form = form(initial=initial)
        else: # Leer
            self.form = form(self.request.POST, instance=instance[self.field]) 

    def getForm(self):
        return self.form

    def is_valid(self):
        return self.form.is_valid()
        
    def save(self):
        formProcessData = CampoFormProcessData(self)
        formProcessData.save()
            
class CampoFormProcessData():
    def __init__(self, form):
        self.form = form
        
    def save(self):
        if self.form.action == "nuevo":
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
        
    def createItem(self):
        self.form.item.sistemaEvaluacion = QueryEvaluationSystem().getEvaluationSystemByCourseSelected(self.form.request)
        self.form.item.orden =  len(QueryItem().getListItemsByEvaluationSystem(self.form.item.sistemaEvaluacion)) + 1
        self.form.item.save()
        
    def editItem(self):
        itemDB = QueryItem().getItemByItem(self.form.itemId)
        itemDB.nombre, itemDB.plazo = self.form.item.nombre, self.form.item.plazo 
        itemDB.save()
        
    def createEvaluation(self):
        item = QueryItem().getItemByItem(self.form.itemId)
        self.form.evaluation.hito = item
        self.form.evaluation.save()
    
    def editEvaluation(self):
        evaluationDB = QueryEvaluation().getEvaluationByEvaluation(self.form.evaluationId)
        evaluationDB.nombre, evaluationDB.evaluador, evaluationDB.miembrosTribunal = self.form.evaluation.nombre, self.form.evaluation.evaluador, self.form.evaluation.miembrosTribunal
        evaluationDB.save()
       
    def createQuestion(self):
        evaluation = QueryEvaluation().getEvaluationByEvaluation(self.form.evaluationId)
        self.form.question.evaluacion = evaluation
        self.form.question.save()
        
    def editQuestion(self):
        questionDB = QueryQuestion().getQuestionByQuestion(self.form.questionId)
        questionDB.pregunta, questionDB.tipoRespuesta = self.form.question.pregunta, self.form.question.tipoRespuesta
    