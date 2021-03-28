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
            CASE url_desc when 'http://223.194.46.212:8730/drama/drama/14/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Romantic Comedy",
            CASE url_desc when 'http://223.194.46.212:8730/drama/drama/15/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Romantic Comedy",
            CASE url_desc when 'http://223.194.46.212:8730/drama/drama/16/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Romantic Comedy",
            CASE url_desc when 'http://223.194.46.212:8730/drama/drama/17/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Romantic Comedy",
            CASE url_desc when 'http://223.194.46.212:8730/drama/genre/2/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Melodrama",
            CASE url_desc when 'http://223.194.46.212:8730/drama/drama/6/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Melodrama",
            CASE url_desc when 'http://223.194.46.212:8730/drama/drama/8/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Melodrama",
            CASE url_desc when 'http://223.194.46.212:8730/drama/drama/7/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Melodrama",
            CASE url_desc when 'http://223.194.46.212:8730/drama/drama/9/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Melodrama",
            CASE url_desc when 'http://223.194.46.212:8730/drama/genre/3/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Action and Thriller",
            CASE url_desc when 'http://223.194.46.212:8730/drama/drama/13/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Action and Thriller",
            CASE url_desc when 'http://223.194.46.212:8730/drama/drama/11/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Action and Thriller",
            CASE url_desc when 'http://223.194.46.212:8730/drama/drama/10/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Action and Thriller",
            CASE url_desc when 'http://223.194.46.212:8730/drama/drama/12/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Action and Thriller",
            CASE url_desc when 'http://223.194.46.212:8730/drama/genre/4/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "History",
            CASE url_desc when 'http://223.194.46.212:8730/drama/drama/1/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "History",
            CASE url_desc when 'http://223.194.46.212:8730/drama/drama/2/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "History",
            CASE url_desc when 'http://223.194.46.212:8730/drama/drama/3/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "History",
            CASE url_desc when 'http://223.194.46.212:8730/drama/drama/4/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "History",
            CASE url_desc when 'http://223.194.46.212:8730/album/3/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Varity",
            CASE url_desc when 'http://223.194.46.212:8730/album/10/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Kpop",
            CASE url_desc when 'http://223.194.46.212:8730/mykocowa/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Mykocowa",
            CASE url_desc when 'http://223.194.46.212:8730/plan/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Plan"
        from weblog
        WHERE ACTION = 'load'
        """)

        # with dbCon:
        #     cursor.execute("""
        #     select
        #     CASE url_desc when 'http://223.194.46.212:8730/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Home",
        #     CASE url_desc when 'http://223.194.46.212:8730/album/1/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Tasty24",
        #     CASE url_desc when 'http://223.194.46.212:8730/drama/genre/1/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Romantic Comedy",
        #     CASE url_desc when 'http://223.194.46.212:8730/drama/genre/2/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Melodrama",
        #     CASE url_desc when 'http://223.194.46.212:8730/drama/genre/3/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Action and Thriller",
        #     CASE url_desc when 'http://223.194.46.212:8730/drama/genre/4/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "History",
        #     CASE url_desc when 'http://223.194.46.212:8730/album/3/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Varity",
        #     CASE url_desc when 'http://223.194.46.212:8730/album/10/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Kpop",
        #     CASE url_desc when 'http://223.194.46.212:8730/mykocowa/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Mykocowa",
        #     CASE url_desc when 'http://223.194.46.212:8730/plan/' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date)) ELSE 0 END AS "Plan"
        #     from weblog
        #     WHERE ACTION = 'load'
        #     """)
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

    return render(request, "chart/chart2byAge.html", {
        'rsSeoul':rsSeoul,
        'rsDaejeon':rsDaejeon,
        'rsBusan': rsBusan,
    })