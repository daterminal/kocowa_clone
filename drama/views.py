from django.shortcuts import render
from django.views.generic import ListView, DetailView
from drama.models import Genre, Drama
from django.core import serializers
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views import View

class GenreLV(ListView):
    model = Genre

class GenreDV(DetailView):
    model = Genre

class DramaDV(DetailView):
    model = Drama


def likes(request):
    if request.is_ajax():  # ajax 방식일 때 아래 코드 실행
        drama_id = request.GET['drama_id']  # 좋아요를 누른 게시물id (drama_id)가지고 오기
        post = Drama.objects.get(id=drama_id)

        if not request.user.is_authenticated:  # 버튼을 누른 유저가 비로그인 유저일 때
            message = "로그인을 해주세요"  # 화면에 띄울 메세지
            context = {'like_count': post.like.count(), "message": message}
            return HttpResponse(json.dumps(context), content_type='application/json')

        user = request.user  # request.user : 현재 로그인한 유저
        if post.like.filter(id=user.id).exists():  # 이미 좋아요를 누른 유저일 때
            post.like.remove(user)  # like field에 현재 유저 추가
            message = "좋아요 취소"  # 화면에 띄울 메세지
        else:  # 좋아요를 누르지 않은 유저일 때
            post.like.add(user)  # like field에 현재 유저 삭제
            message = "좋아요"  # 화면에 띄울 메세지
        # post.like.count() : 게시물이 받은 좋아요 수
        context = {'like_count': post.like.count(), "message": message}
        return HttpResponse(json.dumps(context), content_type='application/json')

def video_detail(request,video_key):
    video = Drama.objects.get(video_key = video_key)
    return render(request,'drama/video_detail.html',{'video':video})
