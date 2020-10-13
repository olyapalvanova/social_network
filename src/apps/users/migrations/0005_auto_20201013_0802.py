# Generated by Django 3.1.1 on 2020-10-13 08:02

from django.db import migrations, models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20201007_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]
