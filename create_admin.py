# create_admin.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ServerTluFood.settings')
# Initialize Django
django.setup()


from AccountEntity.models import AccountEntity

admin_user = AccountEntity.objects.create_superuser(
    username='admin',
    email='admin@gmail.com',
    account_name='admin',
    password='admin'
)
