# Generated by Django 4.0.2 on 2022-02-10 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='organizer',
            table='organizer',
        ),
        migrations.AlterModelTable(
            name='participated',
            table='participated',
        ),
    ]
