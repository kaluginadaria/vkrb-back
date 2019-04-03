from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from vkrb.core.models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'expert', 'is_active', 'is_superuser', 'is_blocked']
    form = UserChangeForm
    ordering = ('email',)
    readonly_fields = ('image_tag',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Персональная информация'), {'fields': ('photo',
                                                  'image_tag',
                                                  'first_name',
                                                  'last_name',
                                                  'age',
                                                  'expert',
                                                  'phone',
                                                  'company',
                                                  'location',
                                                  'experience',
                                                  'occupations',
                                                  'interests',
                                                  'is_blocked'
                                                  )}),
        (('Доступы'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                  'groups', 'user_permissions')}),
        (('Даты'), {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_blocked', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    autocomplete_fields = ('expert',)
