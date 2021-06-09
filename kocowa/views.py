from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from userauth.models import CustomUser
from userauth.admin import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, JsonResponse
from membership.models import CustomUserMembership, Subscription
from .models import Recommend

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
        context = {"message": "로그인을 해주세요"}
        return JsonResponse(context, content_type='application/json')
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
        subscript = Subscription.objects.filter(user_membership_id = memlist[0].id)
        if not subscript:
            #membershiplist에는 있는데 구독이 끝난 회원
            addMember = CustomUserMembership.objects.create(period_day=7, customuser_id_id= user.id)
            addMember.save()
            addSub = Subscription.objects.create(active=True, user_membership_id=addMember.id)
            addSub.save()
        else:
            #구독 중인 회원
            if subscript[0].active:
                context = {'result_msg': "WEEKLY MEMBERSHIP 이미 구독 하였습니다!"}
            else:
                context = {'result_msg': "오류입니다.. 알려주세요.."}
            return JsonResponse(context,content_type="application/json")

    context = {'success_msg':" WEEKLY MEMBERSHIP 구독 신청하였습니다!"}
    return JsonResponse(context,content_type="application/json")

@csrf_exempt
def checkSubscription(request):
    from datetime import datetime, timedelta
    if request.user.is_authenticated:#로그인 한 유저
        user = request.user
        memlist = CustomUserMembership.objects.filter(customuser_id_id = user.id).order_by('-id')[:1]
        if memlist:#membership에 가입한 적이 있는 회원
            subscript = Subscription.objects.filter(user_membership_id = memlist[0].id)
            if subscript:#구독 중인 회원
                subscription = subscript[0]
                due = memlist[0].join_dt + timedelta(days=memlist[0].period_day)
                if datetime.now() > due:
                    #subscription 지우기
                    subscription.delete()
                    context={'result_msg':'멤버십 구독 기간이 만료 되었습니다!'}
                    return JsonResponse(context, content_type="application/json")
                context={}
                return JsonResponse(context, content_type="application/json")
    return render(request,"base.html")

# def play(request):
#     return render(request,"play.html")

def recommend(request):
    import pandas as pd
    import pymysql
    dbCon = pymysql.connect(host='', #서버 정보
                            user='root',
                            password='',
                            db='')
    cursor = dbCon.cursor()

    with dbCon:
        cursor.execute("""
            SELECT *
            FROM (SELECT *
            FROM(SELECT id,member_no,url_desc,ACTION,log_date, 
            CASE 
            WHEN url_desc LIKE '%http://223.194.46.212:8730/photo_video_detail%' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date,member_no))
            WHEN url_desc LIKE '%http://223.194.46.212:8730/drama/video_detail%' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date,member_no)) 
            ELSE 0 END AS "videoStayDuration" 
            from weblog WHERE ACTION = 'load') AS A
            WHERE A.url_desc LIKE '%http://223.194.46.212:8730/photo_video_detail%' OR A.url_desc LIKE '%http://223.194.46.212:8730/drama/video_detail%') AS video_log, 
            (SELECT title,photo_video_time AS video_time,photo_url_desc AS video_url_desc  FROM photo_photo
            UNION ALL 
            SELECT title,drama_video_time AS video_time,drama_url_desc AS video_url_desc FROM drama_drama) AS video
            WHERE video_log.url_desc = video.video_url_desc ORDER BY video_log.log_date, video_log.member_no
        """)
        video_duration = cursor.fetchall()

        cursor.execute("""
            SELECT title FROM photo_photo
            UNION ALL 
            SELECT title FROM drama_drama
        """)
        video_title = cursor.fetchall()

    df = pd.DataFrame(list(video_duration))
    df.columns = ['id', 'member_no', 'url', 'action', 'log_date', 'videoStayDuration', 'title', 'video_time',
                  'video_url']
    df['video_time'] = df['video_time'].apply(lambda x: x.seconds)
    df['videoStayDuration'] = df['videoStayDuration'].astype(float)

    # 평점 계산 (시청완료율)
    df['rating'] = round(df['videoStayDuration'] / df['video_time'],4)
    df.loc[((df['rating'] > 1) & (df['rating'] <= 2)), 'rating'] = 1
    df.loc[df['rating'] > 2, 'rating'] = 0.5

    df = df.dropna(axis=0)# 컨텐츠 시간 없는 거 제외

    # member_no,title,rating만 추출해서 내림차순으로 정렬
    df_sub = df.loc[:, ['member_no', 'title', 'rating']].sort_values(by=['member_no', 'title', 'rating'], axis=0,ascending=False)
    # 중복 제거 (여러 개를 시청한 경우, max값만 남김)
    df_uniq = df_sub.drop_duplicates(['member_no', 'title'], keep='first')

    user_matrix = df_uniq.pivot_table('rating', index='member_no', columns='title')
    user_matrix = user_matrix.fillna(0)

    item_matrix = user_matrix.transpose()

    from sklearn.metrics.pairwise import cosine_similarity
    item_sim = cosine_similarity(item_matrix, item_matrix)
    item_sim_df = pd.DataFrame(data=item_sim, index=user_matrix.columns, columns=user_matrix.columns)
    import numpy as np

    def predict_rating_topsim(ratings_arr, item_sim_arr, n=10):
        pred = np.zeros(ratings_arr.shape)

        for col in range(ratings_arr.shape[1]):
            top_n_items = [np.argsort(item_sim_arr[:, col])[:-n - 1:-1]]
            for row in range(ratings_arr.shape[0]):
                pred[row, col] = item_sim_arr[col, :][top_n_items].dot(ratings_arr[row, :][top_n_items].T)
                pred[row, col] /= np.sum(np.abs(item_sim_arr[col, :][top_n_items]))

        return pred

    ratings_pred2 = predict_rating_topsim(user_matrix.values, item_sim_df.values, n=10)
    ratings_pred2_matrix = pd.DataFrame(data=ratings_pred2, index=user_matrix.index, columns=user_matrix.columns)
    recom_contents = []
    for i in ratings_pred2_matrix.index:
        sample_rating = ratings_pred2_matrix.loc[i, :]
        recom_contents.append(sample_rating[sample_rating > 0].sort_values(ascending=False)[:8].index)

    recom_col = ['recom1', 'recom2', 'recom3', 'recom4', 'recom5', 'recom6', 'recom7', 'recom8']
    recom_df = pd.DataFrame(data=recom_contents, index=user_matrix.index, columns=recom_col)
    # for i in range(recom_df.shape[1]): #열단위 접근
    #     col_name = recom_col[i]
    #     for j in range(recom_df.shape[0]):
    #         col_name = recom_df.iloc[j][i]

    from sqlalchemy import create_engine
    engine = create_engine("mysql://root:password@address/kocowa") #DB서버 정보 입력
    recom_df.to_sql('recommend', con = engine, if_exists='append',index_label='member_no')
    return HttpResponse('')

