# Generated by Django 3.2.7 on 2021-11-23 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='words',
            name='file',
            field=models.FileField(upload_to='usersfile'),
        ),
    ]