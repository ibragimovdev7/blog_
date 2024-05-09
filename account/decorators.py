from django.shortcuts import redirect

def authenticated(my_view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('maqola')
        else:
            return my_view(request, *args, **kwargs)
    return wrapper
