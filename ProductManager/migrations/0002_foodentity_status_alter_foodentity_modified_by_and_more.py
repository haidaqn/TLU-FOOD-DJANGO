# Generated by Django 5.0.2 on 2024-02-14 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductManager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodentity',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='foodentity',
            name='modified_by',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='foodentity',
            name='modified_date',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='restaurantentity',
            name='modified_by',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='restaurantentity',
            name='modified_date',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='typefoodentity',
            name='modified_by',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='typefoodentity',
            name='modified_date',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
