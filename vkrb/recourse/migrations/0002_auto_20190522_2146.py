# Generated by Django 2.0.2 on 2019-05-22 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recourse', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recourse',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='recourse',
            name='expert',
        ),
        migrations.RemoveField(
            model_name='recourse',
            name='gi',
        ),
        migrations.RemoveField(
            model_name='recourse',
            name='keywords',
        ),
        migrations.RemoveField(
            model_name='recourse',
            name='link',
        ),
        migrations.RemoveField(
            model_name='recourse',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='recourse',
            name='reaction_date',
        ),
        migrations.RemoveField(
            model_name='recourse',
            name='si',
        ),
        migrations.RemoveField(
            model_name='recourse',
            name='specialty',
        ),
    ]
