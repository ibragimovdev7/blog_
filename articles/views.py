from django.shortcuts import render
from .models import Maqola
from django.contrib.auth.decorators import login_required



def maqola(request):
    maqolalar = Maqola.objects.all().order_by('-id')  # == SELECT * FROM maqola ORDER BY id desc;
    context = {
        'maqolalar': maqolalar
    }
    return render(
        request=request,
        template_name='maqola.html',
        context=context
    )


def world_news(request):
    w_news = Maqola.objects.filter(tag='world').order_by('-id')
    print(w_news)
    context = {
        'w_news': w_news
    }
    return render(
        request=request,
        template_name='world.html',
        context=context
    )


def local_news(request):
    l_news = Maqola.objects.filter(tag='local').order_by('-id')
    context = {
        'l_news': l_news
    }
    return render(
        request=request,
        template_name='local.html',
        context=context
    )



def sport_news(request):
    s_news = Maqola.objects.filter(tag='sport').order_by('-id')
    context = {
        's_news': s_news
    }
    return render(
        request=request,
        template_name='sport.html',
        context=context
    )


def article_detail(request, id):
    maqola = Maqola.objects.get(id=id)
    context = {
        'maqola': maqola
    }
    return render(
        request=request,
        template_name='article_detail.html',
        context=context
    )
