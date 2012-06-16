# -*- encoding: utf-8 -*-

from django.core.mail import EmailMessage

class EvaluaMailMessage():
    def __init__(self, to, subject):
        self.email = EmailMessage()
        self.email.from_email = 'UJI - Evaluació d\'estudiants de projecte Fi de Grau<provauji@gmail.com>'
        self.email.to = ['landreup@gmail.com', 'aramburu@uji.es', 'lopeza@uji.es']
        self.email.subject = subject
        self.foot = "\n---------------------------------\n"  
        self.foot = "Para: "
        for email in to:
            self.foot += email + ","
        self.foot +=  "\n"
    
    def defineReceivers(self, to):
        self.email.to = ['landreup@gmail.com', 'aramburu@uji.es', 'lopeza@uji.es']
        self.foot = "\n---------------------------------\n"  
        self.foot = "Para: "
        for email in to:
            self.foot += email + ","
        self.foot +=  "\n"
        
    def defineMessage(self, message):
        self.body = message
        
    def send(self):
        self.email.body = self.body + self.foot
        self.email.send()
