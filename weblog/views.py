from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt

def weblog(request):
    context={}
    user = User.objects.get(id = request.user.id)
    if user.is_authenticated:
        memberno = user.id
        membername = user.username
    else:
        redirect('/')

    context["member_no"] = memberno
    context["member_name"] = membername
    context["menuid"] = "weblog"

    import re
    regex_http_ = re.compile(r'^HTTP_.+$')
    regex_content_type = re.compile(r'^CONTENT_TYPE$')
    regex_content_length = re.compile(r'^CONTENT_LENGTH$')
    request_headers = {}
    for header in request.META:
        if regex_http_.match(header) or regex_content_type.match(header) or regex_content_length.match(header):
            request_headers[header] = request.META[header]

    print(request_headers)
    print(type(request_headers))

    # IP
    context["http_host"] = request_headers["HTTP_HOST"]
    print(request_headers["HTTP_HOST"])
    # 디바이스 판단
    context["http_user_agent"] = request_headers["HTTP_USER_AGENT"]
    print(request_headers["HTTP_USER_AGENT"])
    # 웹 url
    context["http_referer"] = request_headers["HTTP_REFERER"]
    print(request_headers["HTTP_REFERER"])

    context["rsHttp"] = request_headers
    print(type(context))
    return render(request, "weblog.html", context)

def weblog_front(request):
    context = {}
    # user = User.objects.get(id = request.user.id)
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        memberno = user.id
        membername = user.username
    else:
        return redirect('/')

    context["member_no"] = memberno
    context["member_name"] = membername
    context["menuid"] = "weblog"


    return render(request, "weblog_front.html", context)

