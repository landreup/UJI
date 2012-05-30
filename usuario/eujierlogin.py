from django.http import HttpResponseForbidden

from mylsm import LSM
from usuario.queries import QueryUser

lsm = LSM()

def eujierlogin(f, name=None):
    if name is None:
        name = f.func_name
        
    def wrapped(*args, **kwargs):
        request = args[0]
        (auth, redirect) = lsm.login(request)
        if not auth :
            return redirect
        (login, redirect) = lsm.get_login(request)
        if not login :
            return redirect
        return f(login=login, *args, **kwargs)
    wrapped.__doc__ = f.__doc__
    return wrapped

def loginFromEujierlogin(request):
    (auth, redirect) = lsm.login(request)
    if not auth :
        return redirect
    (login, redirect) = lsm.get_login(request)
    if not login :
        return redirect
    return login

def eujierlogin_teacher(f, name=None):
    if name is None:
        name = f.func_name
        
    def wrapped(*args, **kwargs):
        request = args[0]
        (auth, redirect) = lsm.login(request)
        if not auth :
            return redirect
        (login, redirect) = lsm.get_login(request)
        if not login :
            return redirect
        
        user = QueryUser().getUserByUserUJI(login)
        if not user:
            return HttpResponseForbidden()
        
        return f(user=user, *args, **kwargs)
    wrapped.__doc__ = f.__doc__
    return wrapped

def eujierlogin_coordinator(f, name=None):
    if name is None:
        name = f.func_name
        
    def wrapped(*args, **kwargs):
        request = args[0]
        (auth, redirect) = lsm.login(request)
        if not auth :
            return redirect
        (login, redirect) = lsm.get_login(request)
        if not login :
            return redirect
        
        coordinator = QueryUser().getUserCoordinatorByUserUJI(login)
        if not coordinator:
            return HttpResponseForbidden()
        
        return f(user=coordinator, *args, **kwargs)
    wrapped.__doc__ = f.__doc__
    return wrapped