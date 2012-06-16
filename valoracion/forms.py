# -*- encoding: utf-8 -*-
from models import Valoracion
from queries import QueryEvaluationForm

from evaluacion.queries import QueryQuestion

from proyecto.controllers import cambiaEstadoProyecto
from valoracion.queries import QueryForm
import datetime

class ValorationForm():
    def __init__(self, request, evaluationForm):
        self.questions = QueryQuestion().getListQuestionsByEvaluation(evaluationForm.evaluacion)
        self.evaluation = evaluationForm.evaluacion
        self.evaluationForm = evaluationForm
        self.valorations = []
        self._indicators = None
        
        questions = QueryQuestion().getListQuestionsByEvaluation(evaluationForm.evaluacion)
        for question in questions:
            valoration = None
            if request.method == 'POST' :
                field = self.fieldName(self.evaluation, question)
                if request.POST.get(field, '') :
                    valoration = int(request.POST.get(field, ''))
            response = self.Response(question, valoration)
            self.valorations.append(response)
        
    def unicodeResponseType(self, field, responseType, valoration):
        if responseType == "A" :
            questionOptions =  u"\t<td><select id=\"id_"+ field +"\" name=\""+ field +"\"><option value=\"1\"  " + ("selected=\"selected\"" if valoration==1 else "") + ">No Apte</option><option value=\"5\" " + ("selected=\"selected\"" if valoration==5 else "") + ">Apte</option></select></td>"
            if self.haveIndicators(): questionOptions += "\n\t<td></td>\n\t<td></td>\n\t<td></td>\n\t<td></td>\n\t<td></td>\n"
            return questionOptions  
        elif responseType == "I":
            return u"\t<td></td>\n\t<td style=\"text-align: center;\"><input id=\"id_"+ field + "\" name=\"" + field + "\" type=\"radio\" value=\"1\" " + ("selected=\"selected\"" if valoration==1 else "") + "/></td>\n\t" + \
                   u"<td style=\"text-align: center;\"><input id=\"id_"+ field + "\" name=\"" + field + "\" type=\"radio\" value=\"2\" " + ("selected=\"selected\"" if valoration==2 else "") + "/></td>\n\t" + \
                   u"<td style=\"text-align: center;\"><input id=\"id_"+ field + "\" name=\"" + field + "\" type=\"radio\" value=\"3\" " + ("selected=\"selected\"" if valoration==3 else "") + "/></td>\n\t" + \
                   u"<td style=\"text-align: center;\"><input id=\"id_"+ field + "\" name=\"" + field + "\" type=\"radio\" value=\"4\" " + ("selected=\"selected\"" if valoration==4 else "") + "/></td>\n\t" + \
                   u"<td style=\"text-align: center;\"><input id=\"id_"+ field + "\" name=\"" + field + "\" type=\"radio\" value=\"5\" " + ("selected=\"selected\"" if valoration==5 else "") + "/></td>\n"
        else:
            return ""
        
    def fieldName(self, evaluation, question):
        return u"evaluacionFormulario" + str(evaluation.id) + u"_pregunta" + str(question.id)
        
    def haveIndicators(self):
        self._indicators 
        if self._indicators == None :
            for valoration in self.valorations:
                if valoration.question.tipoRespuesta == "I" :
                    self._indicators = True
                    return True
            self._indicators = False
            return False
        else:
            return self._indicators
                
        
    def __unicode__(self):
        #return str(len(self.questions))
        ANCHO_COLUMNA = "25"
        htmlForm = "\n<table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" width=\"100%\">\n<tr>\n\t<td></td>\n\t<td></td>\n\t"
        if self.haveIndicators() :
            htmlForm += "<td width=\"" + ANCHO_COLUMNA + "px\" style=\"text-align: center;\">Muy mal</td>\n\t<td width=\"" + ANCHO_COLUMNA + "px\"></td>\n\t<td width=\"" + ANCHO_COLUMNA + "px\"></td>\n\t<td width=\"" + ANCHO_COLUMNA + "px\"></td>\n\t<td width=\"" + ANCHO_COLUMNA + "px\" style=\"text-align: center;\">Muy Bien</td>\n"
        htmlForm += "</tr>\n"
        for valoration in self.valorations :
            question = valoration.question
            field = self.fieldName(self.evaluation, question)
            htmlForm += u"<tr>\n\t<td><label for=\"id_"+ field + "\">" + unicode(question.pregunta) + u"</label></td>\n\t" + self.unicodeResponseType(field, question.tipoRespuesta, valoration.valoration) + u"</tr>\n"
        htmlForm += "</table>"    
        return htmlForm
    
    def isValorationValid(self, response):
        if (response.question.tipoRespuesta == "A") :
            return response.valoration == 1 or response.valoration == 5 
        elif (response.question.tipoRespuesta == "I"):
            return response.valoration > 0 and response.valoration < 6
        else:
            return False
    
    def isAllQuestionsValorated(self):
        for valoration in self.valorations:
            if valoration.valoration == None:
                return False
        return True
    
    def is_valid(self):
        if (self.isAllQuestionsValorated()) :
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
