from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from userauth.models import CustomUser
from userauth.admin import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse

class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')

class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'

def mykocowa(request):
    try:
        user = CustomUser.objects.get(id = request.user.id)
        post_likes = user.likes.all()
        post_loves = user.loves.all()
        context={
            "post_likes":post_likes,
            "post_loves": post_loves,
        }
        return render(request, 'mykocowa.html',context)
    except:
        return render(request, 'registration/login.html')
    
def plan(request):
    print(type(request))
    return render(request,'plan.html')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return HttpResponse(ip ,content_type='text/plain')

