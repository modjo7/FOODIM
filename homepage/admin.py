from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'birthday', 'protein', 'fat', 'carbohydrate', 'vitamin', 'is_staff', 'is_active',)
    list_filter = ('username', 'birthday', 'protein', 'fat', 'carbohydrate', 'vitamin', 'is_staff', 'is_active',) # ('username', 'birthday', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('birthday', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('birthday', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('birthday',)
    ordering = ('birthday',)


admin.site.register(CustomUser, CustomUserAdmin)
