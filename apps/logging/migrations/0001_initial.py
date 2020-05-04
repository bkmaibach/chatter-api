# Generated by Django 2.1.15 on 2020-02-13 21:57

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rest_framework_tracking', '0007_merge_20180419_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIRequestLog',
            fields=[
            ],
            options={
                'verbose_name': 'API request log',
                'verbose_name_plural': 'API request logs',
                'proxy': True,
                'indexes': [],
            },
            bases=('rest_framework_tracking.apirequestlog',),
        ),
    ]
