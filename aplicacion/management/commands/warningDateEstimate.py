# -*- encoding: utf-8 -*-
from django.core.mail import EmailMessage

from django.core.management.base import BaseCommand
import datetime
from proyecto.queries import QueryEstimateDate, QueryProject
from valoracion.queries import QueryForm

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
                for email in QueryProject().getEmailByProjectAndEvaluator(project, rol):
                    to.append(email)
                    cadena += email + u" , "
                email = EmailMessage()
                email.subject = u"Avís data estimada vençuda de " + unicode(item).lower()
                email.from_email = 'UJI - Evaluació d\'estudiants de projecte Fi de Grau<provauji@gmail.com>'
                email.to = ['landreup@gmail.com']
                email.body = "Alumno: " + unicode(project.alumno) + "\nResponsables formulario: " + cadena + "\nROL:" +rol
                email.send()
                print "Se ha enviado un mail"

