# Generated by Django 5.0.3 on 2024-03-20 16:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main.product'),
        ),
    ]