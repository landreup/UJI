# -*- encoding: utf-8 -*-
from django.core.mail import EmailMessage

from django.core.management.base import BaseCommand
import datetime
from proyecto.queries import QueryEstimateDate, QueryProject, QueryJudgeMembers
from valoracion.queries import QueryForm
from settings import SERVER_NAME
from evaluacion.models import Evaluacion

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
                
                body = ""
                body += u"Como " + roles[rol].lower() + u" del alumno " + project.alumno.nombreCompleto() + u" se necesita tu valoración de " + unicode(item).lower() + ".\n"
                body += "\n"
                body += u"Por favor, responde el siguiente formulario para completar la valoración.\n"
                body += "http://" + SERVER_NAME + "/formulari/" + form.codigo + ' \n'
                
                body += "-------------------------------------------\n"
                body += "Alumno: " + unicode(project.alumno) + "\n"
                body += "Responsables formulario (para): " + cadena + "\n"
                body += "ROL:" +rol + "\n"
                body += "Formulario: http://" + SERVER_NAME + "/formulari/" + form.codigo
                
                
                email = EmailMessage()
                email.subject = u"Valoració del " + unicode(item).lower() + " del alumne " + unicode(project.alumno.nombreCompleto())
                email.from_email = 'UJI - Evaluació d\'estudiants de projecte Fi de Grau<provauji@gmail.com>'
                email.to = ['landreup@gmail.com', 'aramburu@uji.es', 'lopeza@uji.es']
                email.body = body
                email.send()
                print "Se ha enviado un mail"

