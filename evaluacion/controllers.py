from models import SistemaEvaluacion, Hito, Evaluacion, Pregunta

from queries import QueryEvaluationSystemTreeComplete, QueryEvaluationSystem

from curso.controllers import cursoSeleccionado, cursoAnteriorAl
  
def editable(request):
    return True

def sistemaEvaluacionSeleccionado(request):
    return QueryEvaluationSystem().getEvaluationSystemByCourseSelected(request)

def listaHitos(evaluationSystem):
    return QueryEvaluationSystemTreeComplete(evaluationSystem).getItems()

def copiarSistemaEvaluacionCursoAnteriorAlCursoActual(request):
    cursoActual = cursoSeleccionado(request)
    cursoAnterior = cursoAnteriorAl(cursoActual)
    
    copyEvaluationSystem(cursoAnterior, cursoActual)

def copyEvaluationSystem(fromCourse, toCourse):
    newEvaluationSystem = SistemaEvaluacion()
    newEvaluationSystem.curso, newEvaluationSystem.estado = toCourse, "D"
    newEvaluationSystem.save()
    if fromCourse :
        fromEvaluationSystemTreeComplete = QueryEvaluationSystemTreeComplete(QueryEvaluationSystem().getEvaluationSystemByCourse(fromCourse))
        for item in fromEvaluationSystemTreeComplete.getItems():
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