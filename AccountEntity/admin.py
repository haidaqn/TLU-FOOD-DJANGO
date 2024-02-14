from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AccountEntityCreationForm, AccountEntityChangeForm
from .models import AccountEntity


class AccountEntityAdmin(UserAdmin):
    add_form = AccountEntityCreationForm
    form = AccountEntityChangeForm
    model = AccountEntity
    list_display = ("email", "is_superuser", "is_staff", "is_active",)
    list_filter = ("is_superuser", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        # Adjusted fields
        ("Permissions", {"fields": ("is_superuser", "is_active",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                # Adjusted fields
                "email", 'username', 'account_name', "password1", "password2", "is_superuser",
                "is_active",
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(AccountEntity, AccountEntityAdmin)
