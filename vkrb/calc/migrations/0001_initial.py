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
            name='Formula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('key', models.CharField(max_length=255, verbose_name='Ключ')),
                ('order', models.PositiveIntegerField(default=0)),
                ('keywords', models.TextField(blank=True, help_text='Через пробел', null=True, verbose_name='Ключевые слова')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attachment.Attachment', verbose_name='Картинка формулы')),
            ],
            options={
                'verbose_name': 'Формула',
                'verbose_name_plural': 'Формулы',
                'ordering': ('order',),
            },
            bases=(vkrb.search.SearchModelMixin, models.Model),
        ),
    ]
