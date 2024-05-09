from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, CodeConfirmation
from django.http import HttpResponse
from .decorators import authenticated

from helpers import sms_send, random_code


def code_conf(request):
    email = request.POST.get('email')
    code = request.POST.get('code')
    user = CustomUser.objects.filter(email=email).first()
    if user:
        obj = CodeConfirmation.objects.filter(user=user, code=code).first()
        if obj:
            user.is_active = True
            user.save()
            login(request, user)
            obj.delete()
            return redirect('maqola')
        return HttpResponse('Email yoki kelgan kod noto`gri!')
    return render(
        request=request,
        template_name='auth/code_confirmation.html'
    )


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        ex_user = CustomUser.objects.filter(email=email).first()
        if ex_user:
            return HttpResponse('<h1>Bu email orqali oldin ro`yxatdan o`tilgan</h1>')
        elif password2 != password1:
            return HttpResponse('<h1>Parollarni to`gri kiriting</h1>')
        else:
            user = CustomUser.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password1
            )
            code = random_code.generate_code()
            sms_send.send_email(email, code)
            CodeConfirmation.objects.create(
                user=user,
                code=code
            )
            return redirect('code_conf')
    return render(
        request=request,
        template_name='auth/register.html'
    )


@authenticated
def log_in(request):
    # if request.user.is_authenticated:
    #     return redirect('maqola')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request=request, email=email, password=password)
        if user:
            login(request=request, user=user)
            return redirect('maqola')
        else:
            return HttpResponse('<h1>Siz password yoki emailni xato kiritingiz!</h1>')
    return render(
        request=request,
        template_name='auth/login.html'
    )


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('maqola')
