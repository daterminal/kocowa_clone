from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from userauth.models import CustomUser
from userauth.admin import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, JsonResponse
from membership.models import CustomUserMembership, Subscription

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
    return render(request,'plan.html')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return HttpResponse(ip ,content_type='text/plain')

@csrf_exempt
def join_weekly_membership(request):
    if not request.user.is_authenticated:
        return render(request,"login.html")
    user = request.user
    memlist = CustomUserMembership.objects.filter(customuser_id_id = user.id).order_by('-id')[:1]
    if not memlist:
        #membership 가입이 처음인 회원
        addMember = CustomUserMembership.objects.create(period_day=7,customuser_id_id=user.id)
        addMember.save()
        addSub = Subscription.objects.create(active=True,user_membership_id=addMember.id)
        addSub.save()
    else:
        #membership에 가입한 적이 있는 회원
        #구독 중인지 확인하기
        subscript = Subscription.objects.get(user_membership_id = memlist[0].id)
        if not subscript:
            #membershiplist에는 있는데 구독이 끝난 회원
            addMember = CustomUserMembership.objects.create(period_day=7, customuser_id_id= user.id)
            addMember.save()
            addSub = Subscription.objects.create(active=True, user_membership_id=addMember.id)
            addSub.save()
        else:
            #구독 중인 회원
            context = {'result_msg': "WEEKLY MEMBERSHIP 이미 구독 하였습니다!"}
            return JsonResponse(context,content_type="application/json")

    context = {'result_msg':" WEEKLY MEMBERSHIP 구독 신청하였습니다!"}
    return JsonResponse(context,content_type="application/json")
