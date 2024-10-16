# Generated by Django 4.1.3 on 2024-09-08 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.TextField()),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('task_count', models.IntegerField()),
                ('user_profile', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='user.userprofile')),
            ],
        ),
    ]
