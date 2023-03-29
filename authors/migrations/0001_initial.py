# Generated by Django 4.1.6 on 2023-03-29 21:11

import authors.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.CharField(default=authors.models.generate_uuid, editable=False, max_length=200, primary_key=True, serialize=False)),
                ('type', models.CharField(default='author', editable=False, max_length=20)),
                ('host', models.CharField(max_length=200)),
                ('displayName', models.CharField(max_length=200, unique=True)),
                ('url', models.CharField(max_length=200)),
                ('github', models.CharField(max_length=200, null=True)),
                ('profileImage', models.CharField(blank=True, max_length=200, null=True)),
                ('customuser', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FollowRequest',
            fields=[
                ('id', models.CharField(default=authors.models.generate_uuid, max_length=200, primary_key=True, serialize=False)),
                ('type', models.CharField(default='Follow', editable=False, max_length=20)),
                ('summary', models.CharField(default='Follow Request', max_length=300)),
                ('status', models.BooleanField(default=False)),
                ('request_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date request came')),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actor', to='authors.author')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='object', to='authors.author')),
            ],
        ),
    ]
