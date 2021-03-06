# Generated by Django 2.0.2 on 2019-04-01 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attachment', '0001_initial'),
        ('core', '0001_initial'),
        ('auth', '0009_alter_user_last_name_max_length'),
        ('expert', '0002_expert_specialty'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='expert',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='expert.Expert', verbose_name='Эксперт'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='attachment.Attachment', verbose_name='Фото'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='pushtoken',
            unique_together={('user', 'session_key')},
        ),
    ]
