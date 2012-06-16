# -*- encoding: utf-8 -*-
import base64
import random
from evaluacion.queries import QueryEvaluation, QueryItem, QueryEvaluationSystem
from valoracion.models import EvaluacionesFormulario, Formulario
from valoracion.queries import QueryForm
from proyecto.models import EstadoProyectoEnCurso
from settings import NUMBER_OF_JUDGE_MEMBERS, SERVER_NAME
from proyecto.queries import QueryProject, QueryJudgeMembers
from aplicacion.mail import EvaluaMailMessage
from evaluacion.models import Evaluacion

def activaFormulario(proyecto, item):
    for rol in QueryEvaluation().getRoles().keys():
        form = QueryForm().getListFormByProjectItemRol(proyecto, item, rol)
        if not form:
            evaluationsItemRol = QueryEvaluation().getListEvaluationsByItemAndRol(item, rol)
            if evaluationsItemRol :
                if rol == "TR" :
                    for i in xrange(1, NUMBER_OF_JUDGE_MEMBERS+1):
                        form = creaFormulario(proyecto, item, rol, evaluationsItemRol, i)
                else:
                    form = creaFormulario(proyecto, item, rol, evaluationsItemRol)

def avisoMail(form):
    item = form.hito
    project = form.proyecto
    rol = form.rol
    subject = u"Reactivació de " + item.nombre.lower() + " del projecte de l'alumne " + unicode(project.alumno.nombreCompleto())
    to = []
    if rol != "TR":
        for email in QueryProject().getEmailByProjectAndEvaluator(project, rol) : to.append(email)
    else:
        miembro = QueryJudgeMembers().getJudgeMemberByProjectAndMemberId(project, form.idMiembro)
        to.append(miembro.getMail())
  
    email = EvaluaMailMessage(to, subject)
    
    roles = Evaluacion().getRoles()
                
    roles["TR"] = "membre del tribunal"
    
    body = ""
    body += "S'ha reactivat la valoració de "+ item.nombre.lower()
    body += u", com a " + roles[rol].lower() + u" del alumne " + project.alumno.nombreCompleto() + u" es necesita la teua valoració.\n"
    body += "\n"
    body += u"Per favor, contesta el siguient formulari per a completar la valoració.\n"
    body += "http://" + SERVER_NAME + "/formulari/" + form.codigo + ' \n'
    
    email.defineMessage(body)
    email.send()

def reActivaFormulario(proyecto, evaluation):
    if evaluation.getEvaluator() == "TR":
        for i in xrange(1, NUMBER_OF_JUDGE_MEMBERS+1):
            form = creaFormulario(proyecto, evaluation.getItem(), evaluation.getEvaluator, [evaluation], i)
            avisoMail(form)
    else:
        form = creaFormulario(proyecto, evaluation.getItem(), evaluation.getEvaluator(), [evaluation])
        avisoMail(form)

def creaFormulario(proyecto, item, rol, evaluationsItemRol, idMiembro=None):
    form = Formulario()
    form.proyecto = proyecto
    form.hito = item
    form.rol = rol
    if idMiembro : form.idMiembro = idMiembro
    form.codigo = aleatoryString()
    form.save()
    for evaluation in evaluationsItemRol:
        evaluationForm = EvaluacionesFormulario()
        evaluationForm.formulario = form
        evaluationForm.evaluacion = evaluation
        evaluationForm.save()
    return form

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