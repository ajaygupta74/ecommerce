# Generated by Django 3.2.7 on 2023-10-15 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='short_content',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
