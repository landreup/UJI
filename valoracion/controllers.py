from models import Formulario, EvaluacionesFormulario

from evaluacion.queries import QueryEvaluation, QueryQuestion

def creaFormulario(proyecto, hito, fechaEstimada):
    for rol in QueryEvaluation().getRoles().keys():
        evaluacionesHitoRol = QueryEvaluation().getListEvaluationsByItemAndRol(hito, rol)
        if evaluacionesHitoRol :
            for email in QueryProject().getEmailByProjectAndEvaluator(project, rol) 
                formulario = Formulario()
                formulario.proyecto = proyecto
                formulario.fechaEstimada = fechaEstimada
                formulario.email = email
                formulario.codigo = "aaaa" #Generar cadena aleatoria
                formulario.save()
                for evaluation in evaluacionesHitoRol:
                    evaluationForm = EvaluacionesFormulario()
                    evaluationForm.form = formulario
                    evaluationForm.evaluacion = evaluation
                    evaluationForm.save()

      