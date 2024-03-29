# Generated by Django 5.0.2 on 2024-02-16 10:07

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ProductManager', '0012_alter_foodentity_quantity_purchased_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BillEntity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_date', models.DateTimeField(null=True)),
                ('finish_date', models.DateTimeField(null=True)),
                ('order_status', models.SmallIntegerField(choices=[(1, 'PENDING'), (2, 'PROCESSING'), (3, 'DELIVERED'), (4, 'CANCELD')], default=1)),
                ('total_amount', models.BigIntegerField()),
                ('name_res', models.CharField(max_length=255)),
                ('finish_time', models.CharField(max_length=255)),
                ('ship_fee', models.IntegerField(default=0)),
                ('code', models.CharField(max_length=255)),
                ('note', models.CharField(max_length=255)),
                ('account_entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('create_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bills_created', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bills_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bill_entity',
            },
        ),
        migrations.CreateModel(
            name='BillDetailEntity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('item', models.CharField(max_length=255)),
                ('food_entity_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProductManager.foodentity')),
                ('bill_entity_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PaymentManager.billentity')),
            ],
            options={
                'db_table': 'bill_detail_entity',
            },
        ),
        migrations.CreateModel(
            name='VoucherEntity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_date', models.DateTimeField(null=True)),
                ('status', models.BooleanField()),
                ('detail', models.CharField(max_length=255)),
                ('expired', models.DateTimeField()),
                ('quantity', models.IntegerField()),
                ('discount', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255, unique=True)),
                ('create_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vouchers_created', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vouchers_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'voucher_entity',
            },
        ),
    ]
