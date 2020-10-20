# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-10-19 10:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('profile_path', models.ImageField(default='profile_pics/prof.jpg', upload_to='media/')),
                ('bio', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('followers', models.ManyToManyField(blank=True, related_name='followers_profile', to='Users.Profile')),
                ('following', models.ManyToManyField(blank=True, related_name='following_profile', to='Users.Profile')),
            ],
        ),
    ]
