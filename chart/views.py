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
    # for i in range(len(rsDuration)):
    #     for j in range(10):
    #         if rsDuration[i][j] == None:
    #             value[j] += 0
    #         elif rsDuration[i][j]:
    #             value[j] += 1

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
