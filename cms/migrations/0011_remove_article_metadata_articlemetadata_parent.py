# Generated by Django 4.1 on 2022-08-14 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0010_articlemetadata_tokens_used'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='metadata',
        ),
        migrations.AddField(
            model_name='articlemetadata',
            name='parent',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.article'),
        ),
    ]
