# Generated by Django 3.1.6 on 2021-02-27 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermembership',
            name='join_dt',
            field=models.DateTimeField(auto_now_add=True, db_column='join_dt'),
        ),
        migrations.AlterField(
            model_name='usermembership',
            name='period_day',
            field=models.IntegerField(db_column='period_day', default=0),
        ),
    ]
