# Generated by Django 4.0.6 on 2022-07-27 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0002_gestion_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gestion',
            old_name='Stageir',
            new_name='Stageir_id',
        ),
    ]
