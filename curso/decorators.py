from curso.queries import QueryCourse
from django.http import HttpResponseServerError

def courseSelected(f, name=None):
    if name is None:
        name = f.func_name
        
    def wrapped(*args, **kwargs):
        request = args[0]
        course = QueryCourse().getCourseSelected(request)
        if not course :
            return HttpResponseServerError()
        return f(course=course, *args, **kwargs)
    wrapped.__doc__ = f.__doc__
    return wrapped