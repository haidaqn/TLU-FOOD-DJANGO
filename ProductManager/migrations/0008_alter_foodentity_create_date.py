# Generated by Django 5.0.2 on 2024-02-16 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductManager', '0007_toppingentity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodentity',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]