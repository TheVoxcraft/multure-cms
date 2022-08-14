# Generated by Django 4.1 on 2022-08-14 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_alter_category_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='metadata',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.articlemetadata'),
        ),
    ]
