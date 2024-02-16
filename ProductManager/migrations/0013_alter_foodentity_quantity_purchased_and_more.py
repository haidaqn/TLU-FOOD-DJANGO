# Generated by Django 5.0.2 on 2024-02-16 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductManager', '0012_alter_foodentity_quantity_purchased_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodentity',
            name='quantity_purchased',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='restaurantentity',
            name='quantity_sold',
            field=models.IntegerField(null=True),
        ),
    ]