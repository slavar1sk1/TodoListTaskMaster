# Generated by Django 4.1.3 on 2024-08-27 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_alter_bronzemodel_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='bronzemodel',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]