# Generated by Django 4.2.18 on 2025-01-17 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='voting',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
