# Generated by Django 3.0.5 on 2020-04-15 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exceldocument',
            name='resultFile',
            field=models.FileField(blank=True, upload_to='documents/%Y/%m/%d'),
        ),
    ]
