from django.shortcuts import get_object_or_404

from models import SistemaEvaluacion, Hito, Evaluacion, Pregunta

from curso.queries import QueryCourse

class QueryEvaluationSystem():
    def getEvaluationSystemByCourse(self, course):
        try:
            return SistemaEvaluacion.objects.get(curso=course)
        except SistemaEvaluacion.DoesNotExist:
            return None
    
    def isEvaluationSystemEnabledByCourse(self, course):
        evaluationSystem = self.getEvaluationSystemByCourse(course)
        if evaluationSystem.isActive(): return True
        return False
    
    def getEvaluationSystemByCourseSelected(self, request):
        return self.getEvaluationSystemByCourse(QueryCourse().getCourseSelected(request))
    
class QueryItem():
    def getItemByItem(self, item):
        return get_object_or_404(Hito, id=item)
    
    def getListItemsByEvaluationSystem(self, evaluationSystem):
        return Hito.objects.filter(sistemaEvaluacion=evaluationSystem).order_by("orden")
    
    def getFirstItemCourse(self, course):
        evaluationSystem = QueryEvaluationSystem().getEvaluationSystemByCourse(course)
        items = self.getListItemsByEvaluationSystem(evaluationSystem)
        return items[0] if items else None
    
    def getNextItem(self, item):
        items = Hito.objects.filter(sistemaEvaluacion=item.sistemaEvaluacion, orden__gt=item.orden).order_by("orden")
        return items[0] if items else None
    
    def getBeforeItem(self, item):
        items = Hito.objects.filter(sistemaEvaluacion=item.sistemaEvaluacion, orden__lt=item.orden).order_by("-orden")
        return items[0] if items else None
    
    def hasTribunalEvaluationThisItem(self, item):
        evaluations = QueryEvaluation().getListEvaluationsByItem(item)
        for evaluation in evaluations:
            if evaluation.isTribunalEvaluator():
                return True
        return False

class QueryEvaluation():
    def getEvaluationByEvaluation(self, evaluation):
        return get_object_or_404(Evaluacion, id=evaluation)
    
    def getListEvaluationsByItem(self, item):
        return Evaluacion.objects.filter(hito=item)
    
    def getListEvaluationsByItemAndRol(self, item, rol):
        return Evaluacion.objects.filter(hito=item, evaluador=rol)
    
    def getRoles(self):
        return Evaluacion().getRoles()

class QueryQuestion():
    def getQuestionByQuestion(self, question):
        return get_object_or_404(Pregunta, id=question)

    def getListQuestionsByEvaluation(self, evaluation):
        return Pregunta.objects.filter(evaluacion=evaluation)
    
class QueryEvaluationSystemTreeComplete():
    def __init__(self, evaluationSystem):
        self.curso = evaluationSystem.curso
        self.estado = evaluationSystem.estado
        self.items = ListItems(evaluationSystem).getList()
    
    def getItems(self):
        return self.items
        
class ListItems():
    def __init__(self, evaluationSystem):
        self.items = QueryItem().getListItemsByEvaluationSystem(evaluationSystem)
        self.list = []
        for item in self.items :
            node = NodeItem(item)
            self.list.append(node)
     
    def getList(self):
        return self.list
       
class NodeItem():
    def __init__(self, item):
        self.id = item.id
        self.item = item
        self.evaluaciones = ListEvaluations(item).getList()

    def __str__(self):
        return self.item.__str__()
    
    def getId(self):
        return self.id
        
    def getItem(self):
        return self.item
    
    def getName(self):
        return self.item.nombre
    
    def getPeriod(self):
        return self.item.plazo
    
    def getOrder(self):
        return self.item.orden
    
    def getEvaluations(self):
        return self.evaluaciones

class ListEvaluations():
    def __init__(self, item):
        self.evaluations = QueryEvaluation().getListEvaluationsByItem(item)
        self.list = []
        for evaluation in self.evaluations :
            node = NodeEvaluation(evaluation)
            self.list.append(node)
        
    def getList(self):
        return self.list
            
class NodeEvaluation():
    def __init__(self, evaluation):
        self.id = evaluation.id
        self.evaluation = evaluation
        self.preguntas = ListQuestions(evaluation).getList()
        
    def __unicode__(self):
        return self.evaluation.__unicode__()   
    
    def getName(self):
        return self.evaluation.nombre
    
    def getEvaluator(self):
        return self.evaluation.evaluador
    
    def getPercentage(self):
        return self.evaluation.porcentaje
    
    def getItem(self):
        return self.evaluation.hito
    
    def getQuestions(self):
        return self.preguntas

class ListQuestions():
    def __init__(self, evaluation):
        self.questions = QueryQuestion().getListQuestionsByEvaluation(evaluation)
    
    def getList(self):
        return self.questions
