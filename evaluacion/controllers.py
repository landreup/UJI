from models import SistemaEvaluacion, Hito, Evaluacion, Pregunta

from queries import QueryEvaluationSystemTreeComplete, QueryEvaluationSystem

from curso.queries import QueryCourse

def editable(request):
    return True and activable(request)

def activable(request):
    evaluationSystem = QueryEvaluationSystem().getEvaluationSystemByCourseSelected(request)
    if evaluationSystem : 
        return not evaluationSystem.isActive()
    else: return False 
    
def listaHitos(evaluationSystem):
    return QueryEvaluationSystemTreeComplete(evaluationSystem).getItems()

def copiarSistemaEvaluacionCursoAnteriorAlCursoActual(request):
    cursoActual = QueryCourse().getCourseSelected(request)
    cursoAnterior = QueryCourse().getCourseBefore(cursoActual)
    
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
                newEvaluation.nombre, newEvaluation.evaluador, newEvaluation.porcentaje, newEvaluation.hito = evaluation.getName(), evaluation.getEvaluator(), evaluation.getPercentage(), newItem 
                newEvaluation.save()
                for question in evaluation.getQuestions():
                    newQuestion = Pregunta()
                    newQuestion.pregunta, newQuestion.tipoRespuesta, newQuestion.evaluacion = question.pregunta, question.tipoRespuesta, newEvaluation
                    newQuestion.save()
