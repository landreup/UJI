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
        
        return f(login=login, *args, **kwargs)
    wrapped.__doc__ = f.__doc__
    return wrapped