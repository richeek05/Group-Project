# Generated by Django 4.1.6 on 2023-03-22 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_like_object'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='object',
            field=models.URLField(max_length=300, null=True),
        ),
    ]
