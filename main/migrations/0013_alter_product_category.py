# Generated by Django 5.0.3 on 2024-03-20 08:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_cart_code_remove_cartproduct_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='main.category'),
            preserve_default=False,
        ),
    ]
