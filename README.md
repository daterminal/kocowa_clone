# kocowa_clone

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

