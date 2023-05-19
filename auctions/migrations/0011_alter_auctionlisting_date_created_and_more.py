# Generated by Django 4.2.1 on 2023-05-19 10:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_auctionlisting_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 19, 15, 44, 59, 692081)),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='title',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 19, 15, 44, 59, 692081)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 19, 15, 44, 59, 693080)),
        ),
    ]
