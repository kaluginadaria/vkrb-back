# Generated by Django 2.0.2 on 2019-04-01 22:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPopular',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=255, verbose_name='Название категории')),
                ('amount', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'популярная категория пользователя',
                'verbose_name_plural': 'популярные категории пользователей',
            },
        ),
        migrations.AlterUniqueTogether(
            name='userpopular',
            unique_together={('user', 'section')},
        ),
    ]
