# Generated by Django 5.0.2 on 2024-02-14 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductManager', '0005_alter_foodentity_star'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodentity',
            name='quantity_purchased',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
