from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .models import ZSUser
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    # 어드민에 관련된 폼들
    form = UserChangeForm
    add_form = UserCreationForm

    # 리스트 관련 설정들
    # 리스트에 띄우는 요소들
    list_display = ('pk', 'email', 'nickname', 'is_active', 'is_superuser', 'date_joined',)
    # 링크로 클릭이 가능한 요소
    list_display_links = ('email',)
    # 요소 필터링 기준
    list_filter = ('date_joined',)
    # 요소 세부 사항의 위치 설정
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('nickname',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser',)}),
    )
    # 새 멤버를 추가할 때 양식
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2',)}),
    )
    # 검색 필드
    search_fields = ('email',)
    # 요소 정렬 기준
    ordering = ('-pk',)
    filter_horizontal = ()


admin.site.register(ZSUser, UserAdmin)
admin.site.unregister(Group)
