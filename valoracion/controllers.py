import base64
import random
from evaluacion.queries import QueryEvaluation, QueryItem, QueryEvaluationSystem
from valoracion.models import EvaluacionesFormulario, Formulario
from proyecto.queries import QueryProject
from valoracion.queries import QueryForm
from proyecto.models import EstadoProyectoEnCurso

def activaFormulario(proyecto, item):
    for rol in QueryEvaluation().getRoles().keys():
        form = QueryForm().getListFormByProjectItemRol(proyecto, item, rol)
        if not form:
            evaluationsItemRol = QueryEvaluation().getListEvaluationsByItemAndRol(item, rol)
            if evaluationsItemRol :
                if rol == "TR" :
                    for email in QueryProject().getEmailByProjectAndEvaluator(proyecto, rol):
                        creaFormulario(proyecto, item, rol, evaluationsItemRol, email)
                else:
                    creaFormulario(proyecto, item, rol, evaluationsItemRol)

def creaFormulario(proyecto, item, rol, evaluationsItemRol, email=None):
    form = Formulario()
    form.proyecto = proyecto
    form.hito = item
    form.rol = rol
    if email : form.email = email
    form.codigo = aleatoryString()
    form.save()
    for evaluation in evaluationsItemRol:
        evaluationForm = EvaluacionesFormulario()
        evaluationForm.formulario = form
        evaluationForm.evaluacion = evaluation
        evaluationForm.save()

def aleatoryString():
    nbits = 100 * 6 + 1
    bits = random.getrandbits(nbits)
    uc = u"%0x" % bits
    newlen = (len(uc) / 2) * 2 # we have to make the string an even length
    ba = bytearray.fromhex(uc[:newlen])
    return base64.urlsafe_b64encode(str(ba))[:100]

def activaValoracion(project):
    evaluationSystem = QueryEvaluationSystem().getEvaluationSystemByCourse(project.curso)
    listItems = QueryItem().getListItemsByEvaluationSystem(evaluationSystem)
    itemStatus = None
    for item in listItems:
        if QueryForm().getListFormByProjectItem(project, item) :
            itemStatus = item
    if itemStatus:
        projectStatus = EstadoProyectoEnCurso()
        projectStatus.proyecto = project
        projectStatus.hito = itemStatus
        projectStatus.save()
        
    project.estado = "L"
    project.save()