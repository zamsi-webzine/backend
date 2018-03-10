from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .models import ZSUser
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('pk', 'email', 'nickname', 'is_active', 'is_superuser', 'date_joined',)
    list_filter = ('date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('nickname',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2',)}),
    )
    search_fields = ('email',)
    ordering = ('-pk',)
    filter_horizontal = ()


admin.site.register(ZSUser, UserAdmin)
admin.site.unregister(Group)
