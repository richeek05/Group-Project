# Generated by Django 4.1.6 on 2023-03-19 20:02

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import posts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('type', models.CharField(default='post', editable=False, max_length=20)),
                ('title', models.CharField(max_length=200)),
                ('id', models.CharField(default=posts.models.generate_uuid, max_length=200, primary_key=True, serialize=False)),
                ('source', models.URLField(blank=True, null=True)),
                ('origin', models.URLField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('content_type', models.CharField(choices=[('text/markdown', 'text/markdown'), ('text/plain', 'text/plain'), ('application/base64', 'application/base64'), ('image/png;base64', 'image/png;base64'), ('image/jpeg;base64', 'image/jpeg;base64')], default='text/plain', max_length=50)),
                ('imagesrc', models.URLField(blank=True, max_length=500, null=True)),
                ('categories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None)),
                ('published', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('visibility', models.CharField(choices=[('PUBLIC', 'public'), ('FRIENDS', 'friends'), ('PRIVATE', 'private')], default='PUBLIC', max_length=100)),
                ('unlisted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted', to='authors.author')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('type', models.CharField(default='Like', editable=False, max_length=200)),
                ('id', models.CharField(default=posts.models.generate_uuid, max_length=200, primary_key=True, serialize=False)),
                ('object', models.URLField(editable=False, null=True)),
                ('object_type', models.CharField(choices=[('post', 'post'), ('comment', 'comment')], default='post', max_length=150)),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.author')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('type', models.CharField(default='comment', editable=False, max_length=200)),
                ('id', models.CharField(default=posts.models.generate_uuid, max_length=200, primary_key=True, serialize=False)),
                ('content_type', models.CharField(choices=[('text/markdown', 'text/markdown'), ('text/plain', 'text/plain')], default='text/plain', max_length=150)),
                ('comment', models.TextField()),
                ('published', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.author')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post')),
            ],
        ),
    ]
