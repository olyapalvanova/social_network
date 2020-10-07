# Generated by Django 3.1.1 on 2020-10-06 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice', models.BooleanField(default=True)),
                ('archived', models.BooleanField(default=False)),
                ('blocked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('read', models.BooleanField()),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.channel')),
            ],
        ),
    ]
