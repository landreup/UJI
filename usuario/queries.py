
from models import Usuario
from django.db.models import Q

class QueryUser:
    def getUserById(self, userId):
        try:
            return Usuario.objects.get(id=userId)
        except Usuario.DoesNotExist:
            return None
    
    def getUserByUserUJI(self, userUJI):
        try:
            return Usuario.objects.get(usuarioUJI=userUJI)
        except:
            return None
    
    def getUserByUserUJIRol(self, userUJI, rol):
        try:
            return Usuario.objects.get(usuarioUJI=userUJI, rol=rol)
        except:
            return None
    
    def getUserCoordinatorByUserUJI(self, userUJI):
        return self.getUserByUserUJIRol(userUJI, "C")
    
    def getListUserByRol(self, rol):
        return Usuario.objects.filter(rol=rol).order_by("apellidos")
    
    def getListOfCoordinator(self):
        return self.getListUserByRol("C")
    
    def getListOfTutor(self):
        return self.getListUserByRol("T")
    
    def getListOfProfessor(self):
        return self.getListUserByRol("P")
    
    def getListOfUser(self):
        return Usuario.objects.all()
    
    def getListOfTutorCoordinator(self):
        return Usuario.objects.filter(Q(rol="T") | Q(rol="C"))
    
    def getMailCoordinator(self):
        mails = []
        for coordinator in self.getListOfCoordinator():
            mails.append(coordinator.getMail())
        return mails
    
    def isTutor(self, userId):
        user = self.getUserById(userId)
        if user :
            return user.rol=="T" or user.rol == "C"
        else:
            return False
        