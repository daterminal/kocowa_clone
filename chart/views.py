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

    # 값이 있는 걸 1로 바꿔서 누적합하면 count로 이용할 수 있을듯
    # for i in range(len(rsDuration)):
    #     for j in range(10):
    #         if rsDuration[i][j] == None:
    #             value[j] += 0
    #         elif rsDuration[i][j]:
    #             value[j] += 1

    return render(request, "chart.html", {
        'rsDuration': value
    })
