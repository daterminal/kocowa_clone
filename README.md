# kocowa_clone
'OTT 서비스 내 이동경로 추적 및 수집 기술 개발'을 주제로 산학연계 SW프로젝트를 진행하기 위해 해외에서 서비스하는 oTT 비디오 스트리밍 사이트 Kocowa를 클론 코딩하였고 이에 대한 코드를 제공한다.

# admin 사이트 로그인 ( url 뒤에 '/admin' 추가 입력 )

ID : user

PASSWORD : 1234

# 프로그램 사용 전
- pip install pymysql
- pip install mysqlclient
- pip install graphene-django
- pip install django-widget-tweaks
- pip install django-cors-headers
- pip install pillow

# 마이그레이션 (app 별로 따로 해야 오류 없이 마이그레이션 가능 합니다.)
- python manage.py makemigrations kocowa
- python manage.py makemigrations photo
- python manage.py makemigrations drama
- python manage.py makemigrations membership
- python manage.py makemigrations userauth

# 로그 발생 코드 위치 
- kocowa_clone/static/assets/js/logfunction.js

# 사용자별 추천 코드 위치
- kocowa_clone/blob/main/photo/templates/photo/album_list.html

---
[시연 영상](https://youtu.be/2qMjZ1xaGyg)
