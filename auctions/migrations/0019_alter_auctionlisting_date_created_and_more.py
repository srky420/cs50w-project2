# Generated by Django 4.2.1 on 2023-05-19 18:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_alter_auctionlisting_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 19, 23, 38, 54, 878831)),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='image',
            field=models.ImageField(default='', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 19, 23, 38, 54, 878831)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 19, 23, 38, 54, 878831)),
        ),
    ]
