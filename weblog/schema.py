import graphene
from graphene_django.types import DjangoObjectType
from .models import Weblog

from datetime import datetime

class LogType(DjangoObjectType):
    class Meta:
        model = Weblog
        fields = ("member_no",
                  "server_desc",
                  "useragent",
                  "url_desc",
                  "action",
                  "client_ip",
                  "log_date")

class WeblogQuery(graphene.ObjectType):
    webloglist = graphene.List(LogType)

    def resolve_webloglist(self, info, **kwargs):
        weblog_list = Weblog.objects.filter()

        return weblog_list

class WeblogCreate(graphene.Mutation):
    # 서버로 보낼 데이터
    class Arguments:
        serverDesc = graphene.String()
        userAgent = graphene.String()
        urlDesc = graphene.String()
        action = graphene.String()
        clientIp = graphene.String()

    weblog = graphene.Field(LogType)

    # Mutation method : DB에 생성
    def mutate(self, info, serverDesc, userAgent, urlDesc, action, clientIp):

        if info.context.user.is_authenticated:
            memberNo = int(info.context.user.id)
        else:
            memberNo = 0

        curtime = datetime.now()
        ymd = curtime.strftime("%Y%m%d")

        weblog = Weblog.objects.create(
            member_no=memberNo,
            server_desc=serverDesc,
            useragent=userAgent,
            url_desc=urlDesc,
            action=action,
            client_ip=clientIp,
            log_date=curtime
        )
        return WeblogCreate(weblog=weblog)

