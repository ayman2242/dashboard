# myapp/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, School, DirectorAuthorization, TeacherAuthorization

# أولاً، تعديل شاشة إدارة المستخدم لتظهر الحقول الخاصة بك
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('username',)
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        # Personal info (يمكن حذفه أو تركه فارغاً)
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active', 'groups'),
        }),
    )
# تسجيل موديلات المدارس والتفويضات
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'wilaya', 'moughatta', 'phone', 'email', 'created_at')
    search_fields = ('name', 'wilaya', 'moughatta')

@admin.register(DirectorAuthorization)
class DirectorAuthorizationAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'authorization_number', 'start_date', 'end_date', 'is_active')
    search_fields = ('user__username', 'school__name', 'authorization_number')
    list_filter = ('is_active', 'start_date', 'end_date')

@admin.register(TeacherAuthorization)
class TeacherAuthorizationAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'specialty', 'authorization_number', 'start_date', 'end_date', 'is_active')
    search_fields = ('user__username', 'school__name', 'specialty', 'authorization_number')
    list_filter = ('is_active', 'start_date', 'end_date')

# اختياري: تسجيل الـ Group لإدارته بسهولة من ال admin
admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('permissions',)
