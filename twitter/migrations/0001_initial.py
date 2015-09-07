# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('about', models.TextField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=140)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TweetProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePhoto',
            fields=[
                ('image_path', models.CharField(max_length=50)),
                ('profile', models.OneToOneField(primary_key=True, serialize=False, to='twitter.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='tweetprofile',
            name='profile',
            field=models.ForeignKey(to='twitter.Profile'),
        ),
        migrations.AddField(
            model_name='tweetprofile',
            name='tweet',
            field=models.ForeignKey(to='twitter.Tweet'),
        ),
        migrations.AddField(
            model_name='profile',
            name='follows',
            field=models.ManyToManyField(related_name='followed_by', to='twitter.Profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='tweets',
            field=models.ManyToManyField(to='twitter.Tweet', through='twitter.TweetProfile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='tweet',
            field=models.ForeignKey(to='twitter.Tweet'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
