# Generated by Django 3.1.1 on 2020-10-13 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0003_auto_20201009_0650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
