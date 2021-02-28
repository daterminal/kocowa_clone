from django.db import models

class Weblog(models.Model):
    member_no = models.IntegerField(db_column='member_no', default=0)
    server_desc = models.CharField(db_column='server_desc', max_length=255)
    useragent = models.CharField(db_column='useragent', max_length=255)
    url_desc = models.CharField(db_column='url_desc', max_length=255)
    action = models.CharField(db_column='action',max_length=255)
    client_ip = models.CharField(db_column='client_ip',max_length=255)
    log_date = models.DateTimeField(db_column='log_date', )

    class Meta:
        managed = False
        db_table = 'weblog'


