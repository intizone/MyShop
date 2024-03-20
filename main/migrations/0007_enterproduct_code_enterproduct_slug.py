# Generated by Django 5.0.3 on 2024-03-20 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_enterproduct_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterproduct',
            name='code',
            field=models.CharField(blank=True, max_length=10, unique=True),
        ),
        migrations.AddField(
            model_name='enterproduct',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]