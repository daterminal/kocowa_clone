from django.views.generic import ListView, DetailView
from photo.models import Album, Photo
from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from membership.models import CustomUserMembership, Subscription
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
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
            post.love.remove(user)  # love field에 현재 유저 삭제
            message = "좋아요 취소"  # 화면에 띄울 메세지
        else:  # 좋아요를 누르지 않은 유저일 때
            post.love.add(user)  # love field에 현재 유저 추가
            message = "좋아요"  # 화면에 띄울 메세지
        # post.love.count() : 게시물이 받은 좋아요 수
        context = {'love_count': post.love.count(), "message": message}
        return HttpResponse(json.dumps(context), content_type='application/json')

def photo_video_detail(request,video_key):
    video = Photo.objects.get(video_key = video_key)
    # member = Membership
    return render(request,'photo/photo_video_detail.html',{'video':video})

# @csrf_exempt
# def episode_list(request):
#     context ={}
#     if request.method == "POST":
#         bodydata = request.body
#         bodyjson = json.loads(bodydata)
#         title = bodyjson['title']
#     # print(title)
#     episode = Photo.objects.filter(title = title).order_by('episode')
#     context['episode_list'] = serializers.serialize('json',episode)
#     print(context['episode_list'])
#     return HttpResponse(context, content_type='application/json')
@csrf_exempt
def checkmembership_photo(request,video_key):
    #video class와 membership 여부를 비교하기 위한 부분
    if not request.user.is_authenticated:
        print('로그인 안한 유저')
        context = {"message": "로그인을 해주세요"}
        return JsonResponse(context, content_type='application/json')
    user = request.user  # request.user : 현재 로그인한 유저
    member = CustomUserMembership.objects.filter(customuser_id_id = user.id).order_by('-id')[:1]

    # CustumUserMembership에 데이터가 없는 경우
    if not member :
        context = {'active':0}
    else:
        subscript = Subscription.objects.filter(user_membership_id=member[0].id)
        # Subscription 데이터가 없는 경우
        if not subscript :
            context = {'active':0}
        else:
            if subscript[0].active:
                active = 1
            else:
                active = 0
            print(active)
            context = {'active': active}
    return JsonResponse(context,content_type="application/json")
