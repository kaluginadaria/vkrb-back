# Generated by Django 2.0.2 on 2019-05-22 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0003_auto_20190523_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='literature',
            name='library',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.CategoryLibrary', verbose_name='Категория'),
        ),
    ]