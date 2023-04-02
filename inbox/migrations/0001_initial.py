# Generated by Django 4.1.6 on 2023-04-02 07:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import inbox.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('authors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('type', models.CharField(default='inbox', editable=False, max_length=200)),
                ('id', models.CharField(default=inbox.models.generate_uuid, max_length=200, primary_key=True, serialize=False)),
                ('object_id', models.CharField(max_length=200, null=True)),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.author')),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
    ]
