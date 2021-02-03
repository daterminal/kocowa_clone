from django.views.generic import ListView, DetailView
from photo.models import Album, Photo

import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

class AlbumLV(ListView):
    model = Album


class AlbumDV(DetailView):
    model = Album


class PhotoDV(DetailView):
    model = Photo

def loves(request):
    if request.is_ajax():  # ajax 방식일 때 아래 코드 실행
        photo_id = request.GET['photo_id']  # 좋아요를 누른 게시물id (photo_id)가지고 오기
        post = Photo.objects.get(id=photo_id)

        if not request.user.is_authenticated:  # 버튼을 누른 유저가 비로그인 유저일 때
            message = "로그인을 해주세요"  # 화면에 띄울 메세지
            context = {'love_count': post.love.count(), "message": message}
            return HttpResponse(json.dumps(context), content_type='application/json')

        user = request.user  # request.user : 현재 로그인한 유저
        if post.love.filter(id=user.id).exists():  # 이미 좋아요를 누른 유저일 때
            post.love.remove(user)  # love field에 현재 유저 추가
            message = "좋아요 취소"  # 화면에 띄울 메세지
        else:  # 좋아요를 누르지 않은 유저일 때
            post.love.add(user)  # love field에 현재 유저 삭제
            message = "좋아요"  # 화면에 띄울 메세지
        # post.love.count() : 게시물이 받은 좋아요 수
        context = {'love_count': post.love.count(), "message": message}
        return HttpResponse(json.dumps(context), content_type='application/json')