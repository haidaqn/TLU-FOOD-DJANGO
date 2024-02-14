from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import AccountEntity


class AccountEntityCreationForm(UserCreationForm):

    class Meta:
        model = AccountEntity
        fields = ("email",'username','account_name')


class AccountEntityChangeForm(UserChangeForm):

    class Meta:
        model = AccountEntity
        fields = ("email",'account_name')