# Generated by Django 2.0.2 on 2019-04-01 22:26

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_serializer.permissions
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attachment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expert', '0001_initial'),
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, verbose_name='Тема обращения')),
                ('question', models.TextField(verbose_name='Текст обращения')),
                ('answer', models.TextField(blank=True, null=True, verbose_name='Ответ эксперта')),
                ('link', models.TextField(null=True, validators=[django.core.validators.URLValidator()], verbose_name='Ссылка на официальный документ')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации вопроса')),
                ('reaction_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время реакции')),
                ('keywords', models.TextField(blank=True, help_text='Через пробел', null=True, verbose_name='Ключевые слова')),
                ('expert', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='expert.Expert', verbose_name='Эксперт')),
                ('gi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='activity.GiItem', verbose_name='ГИ')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recourse.Recourse')),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='attachment.Attachment', verbose_name='Прикрепить фото к ответу эксперта')),
                ('si', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='gi', chained_model_field='gi', null=True, on_delete=django.db.models.deletion.CASCADE, sort=False, to='activity.SiItem', verbose_name='СИ')),
            ],
            options={
                'verbose_name': 'Обсуждение',
                'verbose_name_plural': 'Обсуждения',
            },
        ),
        migrations.CreateModel(
            name='RecourseLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recourse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recourse.Recourse')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Лайк',
                'verbose_name_plural': 'Лайки',
            },
            bases=(django_serializer.permissions.PermissionsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название специализации')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('icon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attachment.Attachment', verbose_name='Иконка')),
            ],
            options={
                'verbose_name': 'Специализация',
                'verbose_name_plural': 'Специализации',
                'ordering': ('order',),
            },
        ),
        migrations.AddField(
            model_name='recourse',
            name='specialty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recourse.Specialty', verbose_name='Специализация обращения'),
        ),
        migrations.AddField(
            model_name='recourse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterUniqueTogether(
            name='recourselike',
            unique_together={('user', 'recourse')},
        ),
    ]
