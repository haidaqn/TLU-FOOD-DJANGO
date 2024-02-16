# Generated by Django 5.0.2 on 2024-02-16 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductManager', '0011_alter_restaurantentity_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodentity',
            name='quantity_purchased',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='restaurantentity',
            name='quantity_sold',
            field=models.IntegerField(default=0),
        ),
    ]