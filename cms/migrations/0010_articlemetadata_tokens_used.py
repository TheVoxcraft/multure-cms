# Generated by Django 4.1 on 2022-08-14 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0009_article_published_alter_article_article_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlemetadata',
            name='tokens_used',
            field=models.IntegerField(default=0),
        ),
    ]
