# Generated by Django 5.0.2 on 2024-02-17 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AccountEntity', '0004_alter_accountentity_img_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountentity',
            name='email',
            field=models.EmailField(max_length=255, null=True, unique=True, verbose_name='email address'),
        ),
    ]
