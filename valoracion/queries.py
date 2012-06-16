# -*- encoding: utf-8 -*-

from django.shortcuts import get_object_or_404
from models import Formulario, EvaluacionesFormulario, Valoracion
from evaluacion.queries import QueryEvaluationSystemTreeComplete, QueryEvaluationSystem, ListItems, NodeItem, ListEvaluations, NodeEvaluation, ListQuestions,\
    QueryQuestion
from settings import NUMBER_OF_JUDGE_MEMBERS

class QueryForm():
    def getListFormByProject(self, project):
        try: 
            return Formulario.objects.filter(proyecto=project)
        except Formulario.DoesNotExist:
            return None 
        
    def getFormByKey(self, key):
        return get_object_or_404(Formulario, codigo=key)
    
    def getListFormByProjectItemRol(self, project, item, rol):
        return Formulario.objects.filter(proyecto=project, hito=item, rol=rol).order_by("-id")
    
    def getListFormByProjectItem(self, project, item):
        return Formulario.objects.filter(proyecto=project, hito=item).order_by("-id")

    def getLastFormsByProjectItemRol(self, project, item, rol):
        listForms = Formulario.objects.filter(proyecto=project, hito=item, rol=rol).order_by("-id")
        if listForms:
            if rol == "TR":
                return listForms[:NUMBER_OF_JUDGE_MEMBERS]
            else:
                return [listForms[0]]
        return []
    
    def getFormsRolByProjectItemRol(self, project, item, rol):
        listForms =  Formulario.objects.filter(proyecto=project, hito=item, rol=rol).order_by("-id")
        i = 0
        formsRol = []
        while (i<len(listForms)):
            forms= []
            if rol == "TR":
                for j in xrange(NUMBER_OF_JUDGE_MEMBERS):
                    forms.append(listForms[i+j])
                i += NUMBER_OF_JUDGE_MEMBERS
            else:
                forms.append(listForms[i])
            formsRol.append(forms)
            i += 1 
            
        return formsRol
        
    def isAllFormsCompleted(self, listForms):
        for form in listForms:
            if not form.fechaValorado:
                return False
        return True if listForms else False
    
    def isAllFormsCompletedOfProjectItem(self, project, item):
        listForms = Formulario.objects.filter(proyecto=project, hito=item)
        return self.isAllFormsCompleted(listForms)

    def isFormCompletedOfProjectItemEvaluator(self, project, item, evaluator):
        listForms = Formulario.objects.filter(proyecto=project, hito=item, rol=evaluator)
        return self.isAllFormsCompleted(listForms)
    
class QueryEvaluationForm():
    def getListEvaluationFormByForm(self, form):
        return EvaluacionesFormulario.objects.filter(formulario=form)
    
    def getEvaluationFormByFormAndEvaluation(self, form, evaluation):
        try:
            return EvaluacionesFormulario.objects.get(formulario=form, evaluacion=evaluation.id)
        except EvaluacionesFormulario.DoesNotExist:
            return None
        
    def getLastEvaluationFormsByProjectAndEvaluation(self, project, evaluation) :
        formsRol = QueryForm().getFormsRolByProjectItemRol(project, evaluation.getItem(), evaluation.getEvaluator())
        evaluationForms = []
        for formRol in formsRol :
            for form in formRol:
                evaluationForm = self.getEvaluationFormByFormAndEvaluation(form, evaluation)
                if evaluationForm :
                    evaluationForms.append(evaluationForm)
            if evaluationForms != [] : return evaluationForms
        return evaluationForms

class QueryValoration():
    def valorationByEvaluationFormAndQuestion(self, evaluationForm, question):
        try:
            return Valoracion.objects.get(evaluacionFormulario=evaluationForm, pregunta=question)
        except Valoracion.DoesNotExist:
            return None
    
    def getListValorationsByEvaluationForm(self, evaluationForm): 
        return Valoracion.objects.filter(evaluacionFormulario=evaluationForm).order_by("pregunta")

class QueryEvaluationSystemTreeCompleteOfProject():
    def __init__(self, project, puntuation=False, rol = None):
        evaluationSystem = QueryEvaluationSystem().getEvaluationSystemByCourse(project.curso)
        tree = QueryEvaluationSystemTreeComplete(evaluationSystem)
        self.list = ListItems(tree.getItems(), project, puntuation, rol).getList()
    
    def getList(self):
        return self.list

class ListItems(ListItems):
    def __init__(self, items, project, puntuation=False, rol=None):
        self.list = []
        for item in items:
            listEvaluations = ListEvaluations(item.getEvaluations(), project, puntuation, rol)
            node = NodeItem(item.getItem(), listEvaluations.getList(), listEvaluations.getStatus())
            self.list.append(node)
            
class NodeItem(NodeItem):
    def __init__(self, item, evaluations, status):
        self.id = item.id
        self.item = item
        self.evaluaciones = evaluations
        self.status = status
        
    def getStatus(self):
        return self.status
    
    def __unicode__(self):
        return unicode(self.item)
        
class ListEvaluations(ListEvaluations):
    def __init__(self, evaluations, project, puntuation, rol=None):
        self.list = []
        self.puntuation = puntuation
        anyUnLock = False
        allComplete = True
        for evaluation in evaluations:
            node = NodeEvaluation(evaluation, project, puntuation, rol)
            if node.getStatus() == "unlock" :
                anyUnLock = True
                allComplete = False
            elif node.getStatus() != "complete":
                allComplete = False
                
            self.list.append(node)
        if anyUnLock :
            self.status = "unlock"
        elif allComplete and len(evaluations)>0:
            self.status = "complete"
        else:
            self.status = "lock"
        
    def getStatus(self):
        return self.status
    
class NodeEvaluation(NodeEvaluation):
    def __init__(self, evaluation, project, puntuation, rol=None):
        self.id = evaluation.id
        self.rol = rol
        self.evaluation = evaluation
        self.evaluationForms = QueryEvaluationForm().getLastEvaluationFormsByProjectAndEvaluation(project, evaluation)
        self.preguntas = QueryQuestion().getListQuestionsByEvaluation(evaluation.id)
        self.value = None
        if puntuation :#and evaluationForm:
            self.preguntas = ListQuestions(self.evaluationForms, evaluation.getQuestions()).getList()
            self.calculatePuntuation()
        
        self.defineStatus()
        
     
    def defineStatus(self):
        forms = []
        for evaluationForm in self.evaluationForms:
            forms.append(evaluationForm.formulario)
        
        if QueryForm().isAllFormsCompleted(forms):
            status = "complete"
        elif len(self.evaluationForms)==0:
            status = "lock"
        else:
            status = "unlock"
        self.status = status
     
    def calculatePuntuation(self):    
        total = 0
        if self.preguntas :
            for question in self.preguntas :
                i = 0.0
                parcial = 0
                for valoration in question.getValoration():
                    parcial += valoration
                    i += 1.0
                if i > 0.0 :
                    total += parcial / i
            self.value = float(total)/len(self.preguntas)
            
    def getStatus(self):
        return self.status
    
    def getItem(self):
        return self.evaluation.hito
    
    def getValue(self):
        return self.value
    
    def getForms(self):
        if self.status == "unlock" :
            if self.evaluation.getEvaluator() == self.rol or self.rol == "C" :
                for evaluationForm in self.evaluationForms:
                    yield evaluationForm.formulario.codigo
            else : yield None
        else : yield None
    
    def __unicode__(self):
        name = unicode(self.evaluation)
        if (self.status == "complete"):
            name += u" Calificació: " + unicode(self.value)
        return name
    
class ListQuestions(ListQuestions):
    def __init__(self, evaluationForms, questions):
        self.list = []
        for question in questions:
            node = NodeQuestion(question)
            for evaluationForm in evaluationForms:
                valoration = QueryValoration().valorationByEvaluationFormAndQuestion(evaluationForm, question)
                if valoration : node.addValoration(valoration)
            self.list.append(node)
            
    def getList(self):
        return self.list

class NodeQuestion():
    def __init__(self, question):
        self.question = question
        self.valorations = []
        
    def addValoration(self, valoration):
        self.valorations.append(valoration.respuesta)
    
    def getValoration(self):
        for valoration in self.valorations:
            yield int(valoration)
    
    def __unicode__(self):
        response = unicode(self.question.pregunta)
        for valoration in self.valorations:
            response += " ("
            response += unicode(valoration)# if self.valoration!=None else "sense evaluar"
            response += ")"
        return response