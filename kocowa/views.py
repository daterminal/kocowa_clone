from django.shortcuts import render

from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return render(request,"home.html")

class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')

class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'

def mykocowa(request):
    try:
        user = User.objects.get(id = request.user.id)
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
    return render(request,'plan.html')
