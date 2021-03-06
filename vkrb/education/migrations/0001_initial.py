# Generated by Django 2.0.2 on 2019-04-01 22:26

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
            name='CatalogItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание технологии')),
                ('mode', models.TextField(blank=True, null=True, verbose_name='Проблематика/специфика применения')),
                ('target', models.TextField(blank=True, null=True, verbose_name='Цель технологии')),
                ('advantages', models.TextField(blank=True, null=True, verbose_name='Преимущества технологии')),
                ('disadvantages', models.TextField(blank=True, null=True, verbose_name='Недостатки')),
                ('application', models.TextField(blank=True, null=True, verbose_name='Применение')),
                ('effect', models.TextField(blank=True, null=True, verbose_name='Потенциальный эффект')),
                ('example', models.TextField(blank=True, null=True, verbose_name='Пример применения технологии')),
                ('result', models.TextField(blank=True, null=True, verbose_name='Результат применения')),
                ('not_applied', models.TextField(blank=True, null=True, verbose_name='Пример, где технология не получила применения')),
                ('reasons', models.TextField(blank=True, null=True, verbose_name='Причины отказа от технологии')),
                ('analogs', models.TextField(blank=True, null=True, verbose_name='Российские и зарубежные аналоги технологи')),
                ('literature', models.TextField(blank=True, null=True, verbose_name='Литература')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('keywords', models.TextField(blank=True, help_text='Через пробел', null=True, verbose_name='Ключевые слова')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catalog_photo', to='attachment.Attachment', verbose_name='Графическое изображение')),
            ],
            options={
                'verbose_name': 'Запись в справочнике',
                'verbose_name_plural': 'Записи в справочнике',
                'ordering': ('order',),
            },
            bases=(vkrb.search.SearchModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CategoryCatalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название категории')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'категория справочника',
                'verbose_name_plural': 'категории справочника',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='CategoryInternalEducation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название категории')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'категория внутреннего обучения',
                'verbose_name_plural': 'категории внутреннего обучения',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='CategoryLibrary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название категории')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_library_photo', to='attachment.Attachment', verbose_name='Иконка категории')),
            ],
            options={
                'verbose_name': 'категория библиотеки',
                'verbose_name_plural': 'категории библиотеки',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='InternalEducation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('location', models.CharField(max_length=255, verbose_name='Место')),
                ('keywords', models.TextField(blank=True, help_text='Через пробел', null=True, verbose_name='Ключевые слова')),
                ('pdf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pdf', to='attachment.Attachment', verbose_name='PDF обучения')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo', to='attachment.Attachment', verbose_name='Картинка обучения')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.CategoryInternalEducation', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Внутреннее обучения',
                'verbose_name_plural': 'Внутренние обучения',
            },
        ),
        migrations.CreateModel(
            name='Literature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('date_of_issued', models.IntegerField(blank=True, default=None, null=True, verbose_name='Год издания')),
                ('author', models.TextField(blank=True, default=None, null=True, verbose_name='Авторы')),
                ('keywords', models.TextField(blank=True, help_text='Через пробел', null=True, verbose_name='Ключевые слова')),
                ('library', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.CategoryLibrary', verbose_name='Категория')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attachment.Attachment', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Литература',
                'verbose_name_plural': 'Литература',
            },
            bases=(vkrb.search.SearchModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Reduction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reduction', models.CharField(max_length=255, verbose_name='Сокращение')),
                ('transcript', models.TextField(verbose_name='Расшифровка')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('library', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.CategoryLibrary', verbose_name='Категория библиотеки')),
            ],
            options={
                'verbose_name': 'сокращение и обозначение',
                'verbose_name_plural': 'сокращения и обозначения',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='ScienceArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('date_of_issued', models.IntegerField(blank=True, default=None, null=True, verbose_name='Год издания')),
                ('author', models.TextField(blank=True, default=None, null=True, verbose_name='Автор')),
                ('keywords', models.TextField(blank=True, help_text='Через пробел', null=True, verbose_name='Ключевые слова')),
                ('problems', models.TextField(blank=True, default=None, null=True, verbose_name='Проблематика')),
                ('decision', models.TextField(blank=True, default=None, null=True, verbose_name='Решение')),
                ('result', models.TextField(blank=True, default=None, null=True, verbose_name='Результат')),
                ('body', models.TextField(blank=True, default=None, null=True, verbose_name='Текст статьи')),
                ('attachment', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachment_articles', to='attachment.Attachment', verbose_name='Приложение')),
                ('library', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.CategoryLibrary', verbose_name='Категория')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo_articles', to='attachment.Attachment', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Научная статья',
                'verbose_name_plural': 'Научные статьи',
            },
            bases=(vkrb.search.SearchModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='categorycatalog',
            name='library',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.CategoryLibrary', verbose_name='Категория библиотеки'),
        ),
        migrations.AddField(
            model_name='categorycatalog',
            name='photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_catalog_photo', to='attachment.Attachment', verbose_name='Иконка категории'),
        ),
        migrations.AddField(
            model_name='catalogitem',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.CategoryCatalog', verbose_name='Категория'),
        ),
    ]
