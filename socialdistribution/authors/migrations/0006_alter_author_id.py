# Generated by Django 4.1.6 on 2023-03-01 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0005_alter_author_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
    ]
