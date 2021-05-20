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

    # 가중치 상위 5개만 골라서 추가
    path.sort(key=lambda x:x[2], reverse=True)
    path = path[:5]

    for _ in range(4):
        q = deque()
        for i in range(len(path)):
            q.append(path[i][1])

        while q:
            x = q.popleft()
            li = []
            for j in range(len(table)):
                if x == table[j][0]:
                    check = False
                    # 이전 노드에 추가된 값인지 확인
                    for z in range(len(path)):
                        if path[z][1] == table[j][1]:
                            check = True
                            break
                    if not check:
                        li.append(table[j])

            li.sort(key=lambda x: x[2], reverse=True)
            if len(li) >= 2:
                li = li[:1]
            else:
                pass

            for i in range(len(li)):
                path.append(li[i])


    return render(request, "chart/chart5.html", {'rs': path})


def chartY(request):
    import pymysql
    dbCon = pymysql.connect(host='223.194.46.212',
                            user='root',
                            password='12345!',
                            db='kocowa')
    cursor = dbCon.cursor()

    with dbCon:
        cursor.execute("""
        SELECT genre, ROUND(AVG(result.reRate),1) AS GenreDur
		FROM(SELECT IF(goal.Rate>200, concat(50,'%'), goal.Rate) AS reRate, genre
        FROM(SELECT concat(ROUND(AVG(videoStayDuration/video.video_time*100),1),'%') AS Rate,
        CASE 
        WHEN title = "Man Who Dies To Live" OR title = "Please Dont Date Him" OR title = "The Spies Who Loved Me" OR title = "Whats Wrong with Secretary Kim" THEN "Romantic Comedy" 
        WHEN title = "Dinner mate" OR title = "Its making crazy Because of yo" OR title = "Find me in your memory" OR title = "W" THEN "Melodrama"
        WHEN title = "Her Private Life" OR title = "Friend our Legend" OR title = "Oh My Ghost" OR title = "Because This is My First Life" THEN "Action And Thriller"
        WHEN title = "Capital Scandal" OR title = "Different Dreams" OR title = "Dr Jin" OR title = "The Emperor" OR title = "The Tale of Nokdu" THEN "History"
        WHEN title = "Cheat On Me If You Can" OR title = "Delayed Justice" OR title = "Homemade Love Story" OR title = "Phoenix 2020" OR title = "Please Dont Date Hime" OR title = "The Game" OR title = "The Penthouse" OR title = "XX" THEN "Trending Now"
        WHEN title = "Home Alone" OR title = "How do you play" OR title = "I was a Car" OR title = "Running Man" OR title = "The Dog I encountered" OR title = "The return of Superman" OR title = "Witches" OR title = "YuHuiyeols Sketchbook" THEN "Reality TV"
        WHEN title = "My Daughter Geum Sa wol Episode 1" OR title = "Lucky Romance Episode 1" OR title = "Lucky Romance Episode 2" OR title = "Twinkle Twinkle Episode 1" OR title = "Twinkle Twinkle Episode 2" OR title = "Coffee Price Episode 1" OR title = "My Daughter Geum Sa wol Episode 2" OR title = "Coffee Price Episode 2" THEN "New Releases"
        WHEN title = "365" OR title = "Nine-Times Time Travel" OR title = "Dr jin" OR title = "Tomorrow With You" OR title = "Eighteen Again" OR title = "Mr Queen" OR title = "Abyss" OR title = "Splash Splash Love" THEN "Travel Through Time"
        WHEN title = "Miss Korea(2013)" OR title = "Couple or Trouble" OR title = "High Kick Season 1" OR title = "High Kick Season 2" OR title = "High Kick Season 3" THEN "KOCOWA K- Classics"
        WHEN title = "Business Trip ShipOhYa" OR title = "Law School" OR title = "Navillera" OR title = "A Familiar Wife" OR title = "Mystic Pop-up Bar" OR title = "SISYPHUS THE MYTH" OR title = "Be Melodramatic" OR title = "Hello, My Twenties!" THEN "Coming Soon"
        WHEN title = "Comedy Big League Episode 1" OR title = "Comedy Big League Episode 2" OR title = "Genre only comedy Episode 1" OR title = "Genre only comedy Episode 2" OR title = "Gagya Episode 1" OR title = "Gagya Episode 2" OR title = "Gagya Episode 3" OR title = "Comedy Big League Episode3" THEN "Spectacular K-TV Award Shows"
        WHEN title = "Sing Again Episode 1" OR title = "Sing Again Episode 2" OR title = "Sing Again Episode 3" OR title = "Begin Again Episode 1" OR title = "Begin Again Episode 2" OR title = "Begin Again Episode 3" OR title = "Friends Song Episode 1" OR title = "Friends Song Episode 2" THEN "All K-Pop"
        ELSE 0 END AS "genre"
        FROM (SELECT *
        FROM(SELECT id,member_no,url_desc,ACTION,log_date,
        CASE 
        WHEN url_desc LIKE '%http://223.194.46.212:8730/photo_video_detail%' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date,member_no))
        WHEN url_desc LIKE '%http://223.194.46.212:8730/drama/video_detail%' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date,member_no)) 
        ELSE 0 END AS "videoStayDuration"
        from weblog WHERE ACTION = 'load') AS A
        WHERE A.url_desc LIKE '%http://223.194.46.212:8730/photo_video_detail%' OR A.url_desc LIKE '%http://223.194.46.212:8730/drama/video_detail%') AS video_log, 
        (SELECT title, TIME_TO_SEC(photo_video_time) AS video_time,photo_url_desc AS video_url_desc  FROM photo_photo
        UNION ALL 
        SELECT title, TIME_TO_SEC(drama_video_time) AS video_time,drama_url_desc AS video_url_desc FROM drama_drama) AS video
        WHERE video_log.url_desc = video.video_url_desc GROUP BY title ORDER BY video_log.log_date, video_log.member_no) AS goal) AS result
        GROUP BY genre
        """)
        rsvideoDuration = cursor.fetchall()

    return render(request, "chart/chartY.html", {
        'rsvideoDuration': rsvideoDuration
    })


def chart2Multi(request):
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
        FROM weblog RIGHT OUTER JOIN time ON (time.hour=HOUR(weblog.log_date) AND log_date BETWEEN DATE_ADD(NOW(),INTERVAL -1 MONTH) AND NOW())
        GROUP BY HOUR
        """)
        rsMemberUseNow = cursor.fetchall()

        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct weblog.member_no)
        FROM weblog RIGHT OUTER JOIN time ON (time.hour=HOUR(weblog.log_date) AND log_date BETWEEN DATE_ADD(NOW(),INTERVAL -2 MONTH) AND NOW())
        GROUP BY HOUR
        """)
        rsMemberUseBefore = cursor.fetchall()

    return render(request, "chart/chart2Multi.html", {
        'rsMemberUseNow': rsMemberUseNow,
        'rsMemberUseBefore': rsMemberUseBefore
    })


def chartYMulti(request):
    import pymysql
    dbCon = pymysql.connect(host='223.194.46.212',
                            user='root',
                            password='12345!',
                            db='kocowa')
    cursor = dbCon.cursor()

    with dbCon:
        cursor.execute("""
        SELECT genre, ROUND(AVG(result.reRate),1) AS GenreDur
		FROM(SELECT IF(goal.Rate>200, concat(50,'%'), goal.Rate) AS reRate, genre
        FROM(SELECT concat(ROUND(AVG(videoStayDuration/video.video_time*100),1),'%') AS Rate,
        CASE 
        WHEN title = "Man Who Dies To Live" OR title = "Please Dont Date Him" OR title = "The Spies Who Loved Me" OR title = "Whats Wrong with Secretary Kim" THEN "Romantic Comedy" 
        WHEN title = "Dinner mate" OR title = "Its making crazy Because of yo" OR title = "Find me in your memory" OR title = "W" THEN "Melodrama"
        WHEN title = "Her Private Life" OR title = "Friend our Legend" OR title = "Oh My Ghost" OR title = "Because This is My First Life" THEN "Action And Thriller"
        WHEN title = "Capital Scandal" OR title = "Different Dreams" OR title = "Dr Jin" OR title = "The Emperor" OR title = "The Tale of Nokdu" THEN "History"
        WHEN title = "Cheat On Me If You Can" OR title = "Delayed Justice" OR title = "Homemade Love Story" OR title = "Phoenix 2020" OR title = "Please Dont Date Hime" OR title = "The Game" OR title = "The Penthouse" OR title = "XX" THEN "Trending Now"
        WHEN title = "Home Alone" OR title = "How do you play" OR title = "I was a Car" OR title = "Running Man" OR title = "The Dog I encountered" OR title = "The return of Superman" OR title = "Witches" OR title = "YuHuiyeols Sketchbook" THEN "Reality TV"
        WHEN title = "My Daughter Geum Sa wol Episode 1" OR title = "Lucky Romance Episode 1" OR title = "Lucky Romance Episode 2" OR title = "Twinkle Twinkle Episode 1" OR title = "Twinkle Twinkle Episode 2" OR title = "Coffee Price Episode 1" OR title = "My Daughter Geum Sa wol Episode 2" OR title = "Coffee Price Episode 2" THEN "New Releases"
        WHEN title = "365" OR title = "Nine-Times Time Travel" OR title = "Dr jin" OR title = "Tomorrow With You" OR title = "Eighteen Again" OR title = "Mr Queen" OR title = "Abyss" OR title = "Splash Splash Love" THEN "Travel Through Time"
        WHEN title = "Miss Korea(2013)" OR title = "Couple or Trouble" OR title = "High Kick Season 1" OR title = "High Kick Season 2" OR title = "High Kick Season 3" THEN "KOCOWA K- Classics"
        WHEN title = "Business Trip ShipOhYa" OR title = "Law School" OR title = "Navillera" OR title = "A Familiar Wife" OR title = "Mystic Pop-up Bar" OR title = "SISYPHUS THE MYTH" OR title = "Be Melodramatic" OR title = "Hello, My Twenties!" THEN "Coming Soon"
        WHEN title = "Comedy Big League Episode 1" OR title = "Comedy Big League Episode 2" OR title = "Genre only comedy Episode 1" OR title = "Genre only comedy Episode 2" OR title = "Gagya Episode 1" OR title = "Gagya Episode 2" OR title = "Gagya Episode 3" OR title = "Comedy Big League Episode3" THEN "Spectacular K-TV Award Shows"
        WHEN title = "Sing Again Episode 1" OR title = "Sing Again Episode 2" OR title = "Sing Again Episode 3" OR title = "Begin Again Episode 1" OR title = "Begin Again Episode 2" OR title = "Begin Again Episode 3" OR title = "Friends Song Episode 1" OR title = "Friends Song Episode 2" THEN "All K-Pop"
        ELSE 0 END AS "genre"
        FROM (SELECT *
        FROM(SELECT id,member_no,url_desc,ACTION,log_date,
        CASE 
        WHEN url_desc LIKE '%http://223.194.46.212:8730/photo_video_detail%' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date,member_no))
        WHEN url_desc LIKE '%http://223.194.46.212:8730/drama/video_detail%' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date,member_no))
        ELSE 0 END AS "videoStayDuration"
        from weblog WHERE ACTION = 'load' AND log_date BETWEEN DATE_ADD(NOW(),INTERVAL -1 MONTH) AND NOW()) AS A
        WHERE A.url_desc LIKE '%http://223.194.46.212:8730/photo_video_detail%' OR A.url_desc LIKE '%http://223.194.46.212:8730/drama/video_detail%') AS video_log, 
        (SELECT title, TIME_TO_SEC(photo_video_time) AS video_time,photo_url_desc AS video_url_desc  FROM photo_photo
        UNION ALL 
        SELECT title, TIME_TO_SEC(drama_video_time) AS video_time,drama_url_desc AS video_url_desc FROM drama_drama) AS video
        WHERE video_log.url_desc = video.video_url_desc GROUP BY title ORDER BY video_log.log_date, video_log.member_no) AS goal) AS result
        GROUP BY genre
        """)
        rsGenreVideoNow = cursor.fetchall()

        cursor.execute("""
        SELECT genre, ROUND(AVG(result.reRate),1) AS GenreDur
		FROM(SELECT IF(goal.Rate>200, concat(50,'%'), goal.Rate) AS reRate, genre
        FROM(SELECT concat(ROUND(AVG(videoStayDuration/video.video_time*100),1),'%') AS Rate,
        CASE 
        WHEN title = "Man Who Dies To Live" OR title = "Please Dont Date Him" OR title = "The Spies Who Loved Me" OR title = "Whats Wrong with Secretary Kim" THEN "Romantic Comedy" 
        WHEN title = "Dinner mate" OR title = "Its making crazy Because of yo" OR title = "Find me in your memory" OR title = "W" THEN "Melodrama"
        WHEN title = "Her Private Life" OR title = "Friend our Legend" OR title = "Oh My Ghost" OR title = "Because This is My First Life" THEN "Action And Thriller"
        WHEN title = "Capital Scandal" OR title = "Different Dreams" OR title = "Dr Jin" OR title = "The Emperor" OR title = "The Tale of Nokdu" THEN "History"
        WHEN title = "Cheat On Me If You Can" OR title = "Delayed Justice" OR title = "Homemade Love Story" OR title = "Phoenix 2020" OR title = "Please Dont Date Hime" OR title = "The Game" OR title = "The Penthouse" OR title = "XX" THEN "Trending Now"
        WHEN title = "Home Alone" OR title = "How do you play" OR title = "I was a Car" OR title = "Running Man" OR title = "The Dog I encountered" OR title = "The return of Superman" OR title = "Witches" OR title = "YuHuiyeols Sketchbook" THEN "Reality TV"
        WHEN title = "My Daughter Geum Sa wol Episode 1" OR title = "Lucky Romance Episode 1" OR title = "Lucky Romance Episode 2" OR title = "Twinkle Twinkle Episode 1" OR title = "Twinkle Twinkle Episode 2" OR title = "Coffee Price Episode 1" OR title = "My Daughter Geum Sa wol Episode 2" OR title = "Coffee Price Episode 2" THEN "New Releases"
        WHEN title = "365" OR title = "Nine-Times Time Travel" OR title = "Dr jin" OR title = "Tomorrow With You" OR title = "Eighteen Again" OR title = "Mr Queen" OR title = "Abyss" OR title = "Splash Splash Love" THEN "Travel Through Time"
        WHEN title = "Miss Korea(2013)" OR title = "Couple or Trouble" OR title = "High Kick Season 1" OR title = "High Kick Season 2" OR title = "High Kick Season 3" THEN "KOCOWA K- Classics"
        WHEN title = "Business Trip ShipOhYa" OR title = "Law School" OR title = "Navillera" OR title = "A Familiar Wife" OR title = "Mystic Pop-up Bar" OR title = "SISYPHUS THE MYTH" OR title = "Be Melodramatic" OR title = "Hello, My Twenties!" THEN "Coming Soon"
        WHEN title = "Comedy Big League Episode 1" OR title = "Comedy Big League Episode 2" OR title = "Genre only comedy Episode 1" OR title = "Genre only comedy Episode 2" OR title = "Gagya Episode 1" OR title = "Gagya Episode 2" OR title = "Gagya Episode 3" OR title = "Comedy Big League Episode3" THEN "Spectacular K-TV Award Shows"
        WHEN title = "Sing Again Episode 1" OR title = "Sing Again Episode 2" OR title = "Sing Again Episode 3" OR title = "Begin Again Episode 1" OR title = "Begin Again Episode 2" OR title = "Begin Again Episode 3" OR title = "Friends Song Episode 1" OR title = "Friends Song Episode 2" THEN "All K-Pop"
        ELSE 0 END AS "genre"
        FROM (SELECT *
        FROM(SELECT id,member_no,url_desc,ACTION,log_date,
        CASE 
        WHEN url_desc LIKE '%http://223.194.46.212:8730/photo_video_detail%' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date,member_no))
        WHEN url_desc LIKE '%http://223.194.46.212:8730/drama/video_detail%' then timestampdiff(second, log_date, LEAD(log_date) over (PARTITION BY action ORDER BY log_date,member_no))
        ELSE 0 END AS "videoStayDuration"
        from weblog WHERE ACTION = 'load' AND log_date BETWEEN DATE_ADD(NOW(),INTERVAL -2 MONTH) AND NOW()) AS A
        WHERE A.url_desc LIKE '%http://223.194.46.212:8730/photo_video_detail%' OR A.url_desc LIKE '%http://223.194.46.212:8730/drama/video_detail%') AS video_log, 
        (SELECT title, TIME_TO_SEC(photo_video_time) AS video_time,photo_url_desc AS video_url_desc  FROM photo_photo
        UNION ALL 
        SELECT title, TIME_TO_SEC(drama_video_time) AS video_time,drama_url_desc AS video_url_desc FROM drama_drama) AS video
        WHERE video_log.url_desc = video.video_url_desc GROUP BY title ORDER BY video_log.log_date, video_log.member_no) AS goal) AS result
        GROUP BY genre
        """)
        rsGenreVideoBefore = cursor.fetchall()

    return render(request, "chart/chartYMulti.html", {
        'rsGenreVideoNow': rsGenreVideoNow,
        'rsGenreVideoBefore': rsGenreVideoBefore
    })

def chartLikeTop(request):
    import pymysql
    dbCon = pymysql.connect(host='223.194.46.212',
                            user='root',
                            password='12345!',
                            db='kocowa')
    cursor = dbCon.cursor()

    with dbCon:
        cursor.execute("""
        SELECT title, COUNT(customuser_id) luvCount
        FROM (SELECT photo_photo_love.customuser_id, photo_photo.title
        FROM photo_photo_love LEFT JOIN photo_photo ON photo_photo_love.photo_id = photo_photo.id) LUV
        GROUP BY title
        UNION ALL
        SELECT title, COUNT(customuser_id)
        FROM (SELECT drama_drama_like.customuser_id, drama_drama.title
        FROM drama_drama_like LEFT JOIN drama_drama ON drama_drama_like.drama_id = drama_drama.id) LIK
        GROUP BY title
        ORDER by luvCount DESC LIMIT 10
        """)
        rsVideoLikeTop = cursor.fetchall()

    return render(request, "chart/chartLikeTop.html", {
        'rsVideoLikeTop': rsVideoLikeTop,
    })


def chartmMulti(request):
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
        FROM membership_customusermembership RIGHT OUTER JOIN time ON (time.hour=HOUR(membership_customusermembership.join_dt) AND join_dt BETWEEN DATE_ADD(NOW(),INTERVAL -1 MONTH) AND NOW())
        GROUP BY hour
        """)
        rsMembershipNow = cursor.fetchall()

        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct membership_customusermembership.customuser_id_id)
        FROM membership_customusermembership RIGHT OUTER JOIN time ON (time.hour=HOUR(membership_customusermembership.join_dt) AND join_dt BETWEEN DATE_ADD(NOW(),INTERVAL -2 MONTH) AND NOW())
        GROUP BY hour
        """)
        rsMembershipBefore = cursor.fetchall()

    return render(request, "chart/chartmMulti.html", {
        'rsMembershipNow': rsMembershipNow,
        'rsMembershipBefore': rsMembershipBefore
    })


def chart2MultiBySex(request):
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
        SELECT TIME.hour, COUNT(distinct A.mno)
        from(SELECT weblog.member_no mno, weblog.log_date log_date
        FROM weblog LEFT OUTER JOIN userauth_customuser
        ON weblog.member_no=userauth_customuser.id
        WHERE userauth_customuser.sexType="WOMAN") A
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(A.log_date) AND log_date BETWEEN DATE_ADD(NOW(),INTERVAL -1 MONTH) AND NOW())
        GROUP BY hour
        """)
        rsWomanNow = cursor.fetchall()

        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct A.mno)
        from(SELECT weblog.member_no mno, weblog.log_date log_date
        FROM weblog LEFT OUTER JOIN userauth_customuser
        ON weblog.member_no=userauth_customuser.id
        WHERE userauth_customuser.sexType="WOMAN") A
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(A.log_date) AND log_date BETWEEN DATE_ADD(NOW(),INTERVAL -2 MONTH) AND NOW())
        GROUP BY hour
        """)
        rsWomanBefore = cursor.fetchall()

        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct A.mno)
        from(SELECT weblog.member_no mno, weblog.log_date log_date
        FROM weblog LEFT OUTER JOIN userauth_customuser
        ON weblog.member_no=userauth_customuser.id
        WHERE userauth_customuser.sexType="MAN") A
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(A.log_date) AND log_date BETWEEN DATE_ADD(NOW(),INTERVAL -1 MONTH) AND NOW())
        GROUP BY hour
        """)
        rsManNow = cursor.fetchall()

        cursor.execute("""
        with recursive time as
        (select 0 as hour union all select hour+1 from time where hour<23)
        SELECT TIME.hour, COUNT(distinct A.mno)
        from(SELECT weblog.member_no mno, weblog.log_date log_date
        FROM weblog LEFT OUTER JOIN userauth_customuser
        ON weblog.member_no=userauth_customuser.id
        WHERE userauth_customuser.sexType="MAN") A
        RIGHT OUTER JOIN TIME ON (TIME.hour=HOUR(A.log_date) AND log_date BETWEEN DATE_ADD(NOW(),INTERVAL -2 MONTH) AND NOW())
        GROUP BY hour
        """)
        rsManBefore = cursor.fetchall()

    return render(request, "chart/chart2MultiBySex.html", {
        'rsWomanNow': rsWomanNow,
        'rsWomanBefore': rsWomanBefore,
        'rsManNow': rsManNow,
        'rsManBefore': rsManBefore
    })


def chartMulti(request):
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
        WHERE ACTION = 'load' AND log_date BETWEEN '2021-03-23 00:00:00' AND '2021-03-30 23:59:59'
        """)
        rsDurationNow = cursor.fetchall()


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
        WHERE ACTION = 'load' AND log_date BETWEEN '2021-03-15 00:00:00' AND '2021-03-22 23:59:59'
        """)
        rsDurationBefore = cursor.fetchall()

    valueNow = [0] * 10
    rsDurationNow = list(rsDurationNow)
    for i in range(len(rsDurationNow)):
        for j in range(10):
            if rsDurationNow[i][j] == None:
                valueNow[j] += 0
            elif rsDurationNow[i][j] > 600:
                valueNow[j] += 0
            else:
                valueNow[j] += rsDurationNow[i][j]

    valueBefore = [0] * 10
    rsDurationBefore = list(rsDurationBefore)
    for i in range(len(rsDurationBefore)):
        for j in range(10):
            if rsDurationBefore[i][j] == None:
                valueBefore[j] += 0
            elif rsDurationBefore[i][j] > 600:
                valueBefore[j] += 0
            else:
                valueBefore[j] += rsDurationBefore[i][j]


    return render(request, "chart/chartMulti.html", {
        'rsDurationNow': valueNow,
        'rsDurationBefore': valueBefore
    })
