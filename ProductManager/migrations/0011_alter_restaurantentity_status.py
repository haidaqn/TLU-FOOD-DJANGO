# Generated by Django 5.0.2 on 2024-02-16 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductManager', '0010_alter_restaurantentity_create_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantentity',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
