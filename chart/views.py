from django.shortcuts import render


def chart(request):
    import pymysql
    dbCon = pymysql.connect(host='223.194.46.212',
                            user='root',
                            password='12345!',
                            db='kocowa')
    cursor = dbCon.cursor()
            with dbCon:
            cursor.execute("""
            select
            CASE url_desc when 'http://223.194.46.212:8730/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Home",
            CASE url_desc when 'http://223.194.46.212:8730/album/1/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Tasty24",
            CASE url_desc when 'http://223.194.46.212:8730/drama/genre/1/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Romantic Comedy",
            CASE url_desc when 'http://223.194.46.212:8730/drama/genre/2/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Melodrama",
            CASE url_desc when 'http://223.194.46.212:8730/drama/genre/3/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Action and Thriller",
            CASE url_desc when 'http://223.194.46.212:8730/drama/genre/4/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "History",
            CASE url_desc when 'http://223.194.46.212:8730/album/3/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Varity",
            CASE url_desc when 'http://223.194.46.212:8730/album/10/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Kpop",
            CASE url_desc when 'http://223.194.46.212:8730/mykocowa/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Mykocowa",
            CASE url_desc when 'http://223.194.46.212:8730/plan/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Plan"
            from weblog
            WHERE ACTION = 'load'
            """)
        rsDuration = cursor.fetchall()

    value = [0] * 10
    rsDuration = list(rsDuration)
    for i in range(len(rsDuration)):
        for j in range(10):
            if rsDuration[i][j] == None:
                value[j] += 0
            elif rsDuration[i][j] > 600:
                value[j] += 0
            else:
                value[j] += rsDuration[i][j]


    return render(request, "chart/chart.html", {
        'rsDuration': value
    })

def chart2(request):
    import pymysql
    dbCon = pymysql.connect(host='223.194.46.212',
                            user='root',
                            password='12345!',
                            db='kocowa')
    cursor = dbCon.cursor()

    with dbCon:
        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct weblog.member_no)
        FROM weblog RIGHT OUTER JOIN time ON (time.hour=HOUR(weblog.log_date))
        GROUP BY hour
        """)
        rsMemberUseByTime = cursor.fetchall()

    return render(request, "chart/chart2.html", {
        'rsMemberUseByTime':rsMemberUseByTime
    })

def chart2bySex(request):
    import pymysql
    dbCon = pymysql.connect(host='223.194.46.212',
                            user='root',
                            password='12345!',
                            db='kocowa')
    cursor = dbCon.cursor()

    with dbCon:
        # 여자
        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct A.mno)
        from(SELECT weblog.member_no mno, weblog.log_date log_date
        FROM weblog LEFT OUTER JOIN userauth_customuser
        ON weblog.member_no=userauth_customuser.id
        WHERE userauth_customuser.sexType="WOMAN") A
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(A.log_date))
        GROUP BY hour
        """)
        rsWoman = cursor.fetchall()
        # 남자
        cursor.execute("""
                with recursive time as
                (select 0 as hour union all select hour+1 from time where hour<23)
                SELECT TIME.hour, COUNT(distinct A.mno)
                from(SELECT weblog.member_no mno, weblog.log_date log_date
                FROM weblog LEFT OUTER JOIN userauth_customuser
                ON weblog.member_no=userauth_customuser.id
                WHERE userauth_customuser.sexType="MAN") A
                RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(A.log_date))
                GROUP BY hour
                """)
        rsMan = cursor.fetchall()

    return render(request, "chart/chart2bySex.html", {
        'rsWoman':rsWoman,
        'rsMan':rsMan
    })

def chart2byAge(request):
    import pymysql
    dbCon = pymysql.connect(host='223.194.46.212',
                            user='root',
                            password='12345!',
                            db='kocowa')
    cursor = dbCon.cursor()

    with dbCon:
        # 10대
        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct A.mno)
        from(SELECT weblog.member_no mno, weblog.log_date log_date
        FROM weblog LEFT OUTER JOIN userauth_customuser
        ON weblog.member_no=userauth_customuser.id
        WHERE userauth_customuser.age BETWEEN 10 AND 19) A
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(A.log_date))
        GROUP BY hour
        """)
        rs10 = cursor.fetchall()
        # 20대
        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct A.mno)
        from(SELECT weblog.member_no mno, weblog.log_date log_date
        FROM weblog LEFT OUTER JOIN userauth_customuser
        ON weblog.member_no=userauth_customuser.id
        WHERE userauth_customuser.age BETWEEN 20 AND 29) A
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(A.log_date))
        GROUP BY hour
                """)
        rs20 = cursor.fetchall()
        # 30대
        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct A.mno)
        from(SELECT weblog.member_no mno, weblog.log_date log_date
        FROM weblog LEFT OUTER JOIN userauth_customuser
        ON weblog.member_no=userauth_customuser.id
        WHERE userauth_customuser.age BETWEEN 30 AND 39) A
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(A.log_date))
        GROUP BY hour
                """)
        rs30 = cursor.fetchall()
        # 40대
        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct A.mno)
        from(SELECT weblog.member_no mno, weblog.log_date log_date
        FROM weblog LEFT OUTER JOIN userauth_customuser
        ON weblog.member_no=userauth_customuser.id
        WHERE userauth_customuser.age BETWEEN 40 AND 49) A
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(A.log_date))
        GROUP BY hour
                """)
        rs40 = cursor.fetchall()

    return render(request, "chart/chart2byAge.html", {
        'rs10':rs10,
        'rs20':rs20,
        'rs30': rs30,
        'rs40': rs40
    })

def chart2byCity(request):
    import pymysql
    dbCon = pymysql.connect(host='223.194.46.212',
                            user='root',
                            password='12345!',
                            db='kocowa')
    cursor = dbCon.cursor()

    with dbCon:
        # 서울
        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct A.mno)
        from(SELECT weblog.member_no mno, weblog.log_date log_date
        FROM weblog LEFT OUTER JOIN userauth_customuser
        ON weblog.member_no=userauth_customuser.id
        WHERE userauth_customuser.city = "Seoul" OR userauth_customuser.city = "서울") A
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(A.log_date))
        GROUP BY hour
        """)
        rsSeoul = cursor.fetchall()
        # 대전
        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct A.mno)
        from(SELECT weblog.member_no mno, weblog.log_date log_date
        FROM weblog LEFT OUTER JOIN userauth_customuser
        ON weblog.member_no=userauth_customuser.id
        WHERE userauth_customuser.city = "Daejeon" OR userauth_customuser.city = "대전") A
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(A.log_date))
        GROUP BY hour
                """)
        rsDaejeon = cursor.fetchall()
        # 부산
        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct A.mno)
        from(SELECT weblog.member_no mno, weblog.log_date log_date
        FROM weblog LEFT OUTER JOIN userauth_customuser
        ON weblog.member_no=userauth_customuser.id
        WHERE userauth_customuser.city = "Busan" OR userauth_customuser.city = "부산") A
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(A.log_date))
        GROUP BY hour
                """)
        rsBusan = cursor.fetchall()

    return render(request, "chart/chart2byCity.html", {
        'rsSeoul':rsSeoul,
        'rsDaejeon':rsDaejeon,
        'rsBusan': rsBusan
    })

# Membership Chart
def chartM(request):
    import pymysql
    dbCon = pymysql.connect(host='223.194.46.212',
                            user='root',
                            password='12345!',
                            db='kocowa')
    cursor = dbCon.cursor()

    with dbCon:
        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct membership_customusermembership.customuser_id_id)
        FROM membership_customusermembership RIGHT OUTER JOIN time ON (time.hour=HOUR(membership_customusermembership.join_dt))
        GROUP BY hour
        """)
        rsMembershipUseByTime = cursor.fetchall()

    return render(request, "chart/membership_chart.html", {
        'rsMembershipUseByTime':rsMembershipUseByTime
    })

def chartM_Sex(request):
    import pymysql
    dbCon = pymysql.connect(host='223.194.46.212',
                            user='root',
                            password='12345!',
                            db='kocowa')
    cursor = dbCon.cursor()

    with dbCon:
        # 여자
        cursor.execute("""
            with recursive time as
            (select 0 as hour union all select hour+1 from time where hour<23)
            SELECT TIME.hour, COUNT(distinct A.mno)
            from(SELECT membership_customusermembership.customuser_id_id mno, membership_customusermembership.join_dt join_dt
            FROM membership_customusermembership LEFT OUTER JOIN userauth_customuser
            ON membership_customusermembership.customuser_id_id=userauth_customuser.id
            WHERE userauth_customuser.sexType="WOMAN") A
            RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(A.join_dt))
            GROUP BY hour
        """)
        rsWoman = cursor.fetchall()

        # 남자
        cursor.execute("""
                with recursive time as
                (select 0 as hour union all select hour+1 from time where hour<23)
                SELECT TIME.hour, COUNT(distinct B.mno)
                from(SELECT membership_customusermembership.customuser_id_id mno, membership_customusermembership.join_dt join_dt
                FROM membership_customusermembership LEFT OUTER JOIN userauth_customuser
                ON membership_customusermembership.customuser_id_id=userauth_customuser.id
                WHERE userauth_customuser.sexType="MAN") B
                RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(B.join_dt))
                GROUP BY hour
                """)
        rsMan = cursor.fetchall()

    return render(request, "chart/membership_chart_sex.html", {
        'rsWoman':rsWoman,
        'rsMan':rsMan
    })

def chartM_Age(request):
    import pymysql
    dbCon = pymysql.connect(host='223.194.46.212',
                            user='root',
                            password='12345!',
                            db='kocowa')
    cursor = dbCon.cursor()

    with dbCon:
        # 10대
        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct A.mno)
        from(SELECT membership_customusermembership.customuser_id_id mno, membership_customusermembership.join_dt join_dt
        FROM membership_customusermembership LEFT OUTER JOIN userauth_customuser
        ON membership_customusermembership.customuser_id_id=userauth_customuser.id
        WHERE userauth_customuser.age BETWEEN 10 AND 19) A
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(A.join_dt))
        GROUP BY hour
        """)
        rs10 = cursor.fetchall()
        # 20대
        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct B.mno)
        from(SELECT membership_customusermembership.customuser_id_id mno, membership_customusermembership.join_dt join_dt
        FROM membership_customusermembership LEFT OUTER JOIN userauth_customuser
        ON membership_customusermembership.customuser_id_id=userauth_customuser.id
        WHERE userauth_customuser.age BETWEEN 20 AND 29) B
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(B.join_dt))
        GROUP BY hour
                """)
        rs20 = cursor.fetchall()
        # 30대
        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct C.mno)
        from(SELECT membership_customusermembership.customuser_id_id mno, membership_customusermembership.join_dt join_dt
        FROM membership_customusermembership LEFT OUTER JOIN userauth_customuser
        ON membership_customusermembership.customuser_id_id=userauth_customuser.id
        WHERE userauth_customuser.age BETWEEN 30 AND 39) C
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(C.join_dt))
        GROUP BY hour
                """)
        rs30 = cursor.fetchall()
        # 40대
        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct D.mno)
        from(SELECT membership_customusermembership.customuser_id_id mno, membership_customusermembership.join_dt join_dt
        FROM membership_customusermembership LEFT OUTER JOIN userauth_customuser
        ON membership_customusermembership.customuser_id_id=userauth_customuser.id
        WHERE userauth_customuser.age BETWEEN 40 AND 49) D
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(D.join_dt))
        GROUP BY hour
                """)
        rs40 = cursor.fetchall()

    return render(request, "chart/membership_chart_age.html", {
        'rs10': rs10,
        'rs20': rs20,
        'rs30': rs30,
        'rs40': rs40
    })

def chartM_City(request):
    import pymysql
    dbCon = pymysql.connect(host='223.194.46.212',
                            user='root',
                            password='12345!',
                            db='kocowa')
    cursor = dbCon.cursor()

    with dbCon:
        # 서울
        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct A.mno)
        from(SELECT membership_customusermembership.customuser_id_id mno, membership_customusermembership.join_dt join_dt
        FROM membership_customusermembership LEFT OUTER JOIN userauth_customuser
        ON membership_customusermembership.customuser_id_id=userauth_customuser.id
        WHERE userauth_customuser.city = "Seoul" OR userauth_customuser.city = "서울") A
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(A.join_dt))
        GROUP BY hour
        """)
        rsSeoul = cursor.fetchall()
        # 대전
        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct B.mno)
        from(SELECT membership_customusermembership.customuser_id_id mno, membership_customusermembership.join_dt join_dt
        FROM membership_customusermembership LEFT OUTER JOIN userauth_customuser
        ON membership_customusermembership.customuser_id_id=userauth_customuser.id
        WHERE userauth_customuser.city = "Daejeon" OR userauth_customuser.city = "대전") B
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(B.join_dt))
        GROUP BY hour
                """)
        rsDaejeon = cursor.fetchall()
        # 부산
        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct C.mno)
        from(SELECT membership_customusermembership.customuser_id_id mno, membership_customusermembership.join_dt join_dt
        FROM membership_customusermembership LEFT OUTER JOIN userauth_customuser
        ON membership_customusermembership.customuser_id_id=userauth_customuser.id
        WHERE userauth_customuser.city = "Busan" OR userauth_customuser.city = "부산") C
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(C.join_dt))
        GROUP BY hour
                """)
        rsBusan = cursor.fetchall()

    return render(request, "chart/membership_chart_city.html", {
        'rsSeoul':rsSeoul,
        'rsDaejeon':rsDaejeon,
        'rsBusan': rsBusan
    })

def chart3(request):
    import pymysql
    from collections import deque
    dbCon = pymysql.connect(host='223.194.46.212',
                            user='root',
                            password='12345!',
                            db='kocowa')
    cursor = dbCon.cursor()

    with dbCon:
        cursor.execute("""
            SELECT member_no, url_desc, log_date
            FROM weblog
            WHERE url_desc LIKE "http://223%"
            order BY member_no
        """)

    contents = cursor.fetchall()
    contents = list(contents)

    od = []

    # 전후 페이지가 동일하면 pass 아니라면 리스트에 추가
    for i in range(len(contents) - 1):
        if contents[i][1] == contents[i + 1][1]:
            continue
        else:
            od.append([contents[i][1], contents[i + 1][1]])

    # 중복 행 개수를 카운트해서 가중치로 표현
    od_sum = []
    for i in range(len(od)):
        od_sum.append(od[i][0] + " " + od[i][1])

    count = {}
    for i in od_sum:
        try:
            count[i] += 1
        except:
            count[i] = 1

    table = []
    for k, v in count.items():
        o, d = k.split(' ')
        table.append([o, d, v])

    # 가중치가 1이라면 시각화 편의를 위해 제거
    idx = 0
    for i in range(len(table)):
        if table[idx][2] == 1:
            del table[idx]
        else:
            idx += 1


    # O와 D가 같은 데이터 제거 및 Home에서 시작하는 데이터를 Path에 추가
    path = []
    idx = 0
    for i in range(len(table)):
        if table[idx][0] == 'http://223.194.46.212:8730/':
            path.append(table[idx])
            del table[idx]
        elif table[idx][1] == 'http://223.194.46.212:8730/':
            del table[idx]
        else:
            idx += 1

    # 가중치 상위 10개만 골라서 추가
    path.sort(key=lambda x:x[2], reverse=True)
    path = path[:10]

    for _ in range(3):
        q = deque()
        for i in range(len(path)):
            q.append(path[i][1])

        while q:
            x = q.popleft()
            li = []
            for j in range(len(table)):
                if x == table[j][0]:
                    check = 0
                    for z in range(len(path)):
                        if path[z][1] == table[j][1]:
                            check = 1
                            break
                    if not check:
                        li.append(table[j])

            li.sort(key=lambda x: x[2], reverse=True)
            if len(li) > 2:
                li = li[:3]
            else:
                pass
            for i in range(len(li)):
                path.append(li[i])


    return render(request, "chart/chart4.html", {'rs': path})
