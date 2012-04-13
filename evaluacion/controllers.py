from models import SistemaEvaluacion, Hito, Evaluacion, Pregunta

from queries import QueryEvaluationSystemTreeComplete, QueryEvaluationSystem
  
def editable(request):
    return True
  
def listaHitos(request):
    evaluationSystem = QueryEvaluationSystem().getEvaluationSystemByCourseSelected(request)
    return QueryEvaluationSystemTreeComplete(evaluationSystem).getItems()

def CopyEvaluationSystem(fromCourse, toCourse):
    newEvaluationSystem = SistemaEvaluacion()
    newEvaluationSystem.curso, newEvaluationSystem.estado = toCourse, "D"
    newEvaluationSystem.save()
    if fromCourse :
        fromEvaluationSystem = QueryEvaluationSystem().getEvaluationSystemByCourse(fromCourse)
        for item in fromEvaluationSystem.getItems():
            newItem = Hito()
            newItem.nombre, newItem.plazo, newItem.orden, newItem.sistemaEvaluacion = item.getName(), item.getPeriod(), item.getOrder(), newEvaluationSystem 
            newItem.save()
            for evaluation in item.getEvaluations() :
                newEvaluation = Evaluacion()
                newEvaluation.nombre, newEvaluation.evaluador, newEvaluation.miembrosTribunal, newEvaluation.hito = evaluation.getName(), evaluation.getEvaluator(), evaluation.getTribunalMembers(), newItem 
                newEvaluation.save()
                for question in evaluation.getQuestions():
                    newQuestion = Pregunta()
                    newQuestion.pregunta, newQuestion.tipoRespuesta, newQuestion.evaluacion = question.pregunta, question.tipoRespuesta, newEvaluation
                    newQuestion.save()
#class EvaluationSystemCopy():
#    def fromCourse(self, course):
#        
#    def toNewEvaluationSystemInCourse(self, course):
#        newEvaluationSystem = SistemaEvaluacion()
#        newEvaluationSystem.curso, newEvaluationSystem.estado = course, "D"
#        newEvaluationSystem.save()
#        
#        if self.fromEvaluationSystem :
#            for item in self.fromEvaluationSystem.getItems():
#                newItem = Hito()
#                newItem.nombre, newItem.plazo, newItem.orden, newItem.sistemaEvaluacion = item.getName(), item.getPeriod(), item.getOrder(), newEvaluationSystem 
#                newItem.save()
#                for evaluation in item.getEvaluations() :
#                    newEvaluation = Evaluacion()
#                    newEvaluation.nombre, newEvaluation.evaluador, newEvaluation.miembrosTribunal, newEvaluation.hito = evaluation.getName(), evaluation.getEvaluator(), evaluation.getTribunalMembers(), newItem 
#                    newEvaluation.save()
#                    for question in evaluation.getQuestions():
#                        newQuestion = Pregunta()
#                        newQuestion.pregunta, newQuestion.tipoRespuesta, newQuestion.evaluacion = question.pregunta, question.tipoRespuesta, newEvaluation
#                        newQuestion.save()