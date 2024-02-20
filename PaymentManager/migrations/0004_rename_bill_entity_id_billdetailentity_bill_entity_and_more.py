# Generated by Django 5.0.2 on 2024-02-20 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PaymentManager', '0003_rename_item_billdetailentity_item_list'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billdetailentity',
            old_name='bill_entity_id',
            new_name='bill_entity',
        ),
        migrations.RenameField(
            model_name='billdetailentity',
            old_name='food_entity_id',
            new_name='food_entity',
        ),
        migrations.RemoveField(
            model_name='billentity',
            name='name_res',
        ),
        migrations.AlterField(
            model_name='billdetailentity',
            name='item_list',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='billentity',
            name='order_status',
            field=models.SmallIntegerField(choices=[(1, 'PENDING'), (2, 'PROCESSING'), (3, 'DELIVERED'), (4, 'CANCELED')], default=1),
        ),
    ]