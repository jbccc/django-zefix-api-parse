# Generated by Django 3.2.7 on 2021-09-10 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_auto_20210910_0220'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestDb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('oui', models.CharField(max_length=10)),
            ],
        ),
    ]
