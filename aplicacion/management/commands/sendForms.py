# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand
import datetime
from proyecto.queries import QueryEstimateDate, QueryProject, QueryJudgeMembers
from valoracion.queries import QueryForm
from settings import SERVER_NAME
from evaluacion.models import Evaluacion
from aplicacion.mail import EvaluaMailMessage

class Command(BaseCommand):
    def handle(self, *args, **options):
        today = datetime.date.today()
        
        listEstimateDate = QueryEstimateDate().getListEstimateDateByDate(today)
        
        for estimateDate in listEstimateDate:
            project = estimateDate.proyecto
            item = estimateDate.hito
            listForm = QueryForm().getListFormByProjectItem(project, item)
            for form in listForm:
                rol = form.rol
                to = []
                cadena = u""
                if rol == "TR" :
                    miembro = QueryJudgeMembers().getJudgeMemberByProjectAndMemberId(project, form.idMiembro)
                    email = miembro.getMail()
                    to.append(email)
                    cadena += email
                else:
                    for email in QueryProject().getEmailByProjectAndEvaluator(project, rol):
                        to.append(email)
                        cadena += email + u" , "
                
                roles = Evaluacion().getRoles()
                
                roles["TR"] = "membre del tribunal"
                
                body = ""
                body += u"Com a " + roles[rol].lower() + u" del alumne " + project.alumno.nombreCompleto() + u" es necesita la teua valoració de " + unicode(item).lower() + ".\n"
                body += "\n"
                body += u"Per favor, contesta el siguient formulari per a completar la valoració.\n"
                body += "http://" + SERVER_NAME + "/formulari/" + form.codigo + ' \n'
                 
                subject = u"Valoració del " + unicode(item).lower() + " del alumne " + unicode(project.alumno.nombreCompleto())
                email = EvaluaMailMessage(to, subject)
                
                email.defineMessage(body)
                email.send()
                print "Se ha enviado un mail"

