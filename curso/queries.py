from models import Curso

class Course:
    def getByCourseSelected(self, request):
        return QueryCourse().getCourseSelected(request)

class QueryCourse:
    
    def getCourseByCourse(self, course):
        try: 
            return Curso.objects.get(curso=course)
        except:
            return None
    
    def getLastCourse(self):
        listCourse = Curso.objects.order_by("-id")
        if  len(listCourse)>0:
            return listCourse[0]
        else:
            return None
    
    def getCourseSelected(self, request):
        if 'curso' in request.session :
            if request.session['curso'] != None : 
                course = request.session['curso']
            else:
                course = QueryCourse().getLastCourse()
        else:
            course = QueryCourse().getLastCourse()
        request.session['curso'] = course
        return course
    
    def _getListCourse(self):
        return Curso.objects.all().order_by("id")
    
    def getListCourse(self, request):
        listCourse = self._getListCourse()
    
        courseSelected = self.getCourseSelected(request)
    
        for course in listCourse:
            if ( course.curso == courseSelected.curso ) :
                course.esActual = True
        return listCourse
    
    def existCourse(self, course):
        return Curso.objects.filter(curso=course) != None
    
    def getCourseBefore(self, courseSelected):
        return self.getCourseByCourse(courseSelected.curso-1)
    
    def isActual(self, course):
        return self.getLastCourse() == course

    def isActualCourseSelected(self, request):
        return self.isActual(self.getCourseSelected(request))