# Generated by Django 4.2.1 on 2023-05-21 14:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0029_alter_auctionlisting_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 21, 19, 13, 20, 445239)),
        ),
        migrations.AlterField(
            model_name='bid',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 21, 19, 13, 20, 445239)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 21, 19, 13, 20, 445239)),
        ),
    ]
