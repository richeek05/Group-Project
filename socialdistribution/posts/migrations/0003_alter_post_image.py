# Generated by Django 4.1.6 on 2023-03-02 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_rename_id_comment_comment_id_rename_id_like_like_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='blank_profile.png', null=True, upload_to='post_images'),
        ),
    ]