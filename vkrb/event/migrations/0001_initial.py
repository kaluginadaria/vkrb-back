# Generated by Django 2.0.2 on 2019-04-01 22:26

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion
import vkrb.search


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attachment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.TextField(verbose_name='Тема')),
                ('start', models.DateTimeField(help_text='Если событие одним днем, заполните только старт.', verbose_name='Старт события')),
                ('end', models.DateTimeField(blank=True, null=True, verbose_name='Конец события')),
                ('location', models.CharField(max_length=255, verbose_name='Место')),
                ('pdf', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='attachment.Attachment', verbose_name='Загрузка PDF файла')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'События',
            },
            bases=(vkrb.search.SearchModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('color', colorfield.fields.ColorField(default='#FF0000', max_length=18, verbose_name='Цвет рамки в календаре')),
            ],
            options={
                'verbose_name': 'Тип события',
                'verbose_name_plural': 'Типы событий',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='event.EventType', verbose_name='Тип события'),
        ),
    ]
