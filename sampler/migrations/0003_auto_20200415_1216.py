# Generated by Django 3.0.5 on 2020-04-15 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampler', '0002_exceldocument_resultfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exceldocument',
            name='resultFile',
        ),
        migrations.AlterField(
            model_name='exceldocument',
            name='docFile',
            field=models.FileField(upload_to='documents'),
        ),
    ]
