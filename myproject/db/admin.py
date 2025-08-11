from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser, School, DirectorAuthorization, TeacherAuthorization


# Custom User Admin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'nni', 'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'nni', 'phone')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'nni', 'phone', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active', 'groups'),
        }),
    )


# School Admin


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('nomEcole', 'wilaya', 'nomMoughatta', 'numTel', 'code', 'dateAjout')
    search_fields = ('nomEcole', 'wilaya', 'nomMoughatta', 'numTel', 'code')
    list_filter = ('wilaya', 'nomMoughatta', 'dateAjout')



# Director Authorization Admin


@admin.register(DirectorAuthorization)
class DirectorAuthorizationAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'nomEcole', 'autorisationNum', 'dateDebut', 'dateFin', 'typeAutorisationDirige')
    search_fields = ('user__username', 'school__nomEcole', 'autorisationNum', 'nni', 'nom')
    list_filter = ('school', 'wilaya', 'nomMoughatta', 'dateDebut', 'dateFin', 'typeAutorisationDirige')



# Teacher Authorization Admin


@admin.register(TeacherAuthorization)
class TeacherAuthorizationAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'specialiteDiplome', 'codeAE', 'dateDebut', 'dateFin', 'is_active')
    search_fields = ('user__username', 'school__nomEcole', 'specialiteDiplome', 'nni', 'nom', 'codeAE')
    list_filter = ('school', 'is_active', 'dateDebut', 'dateFin', 'specialiteDiplome')


# -------------------------
# Group Admin
# -------------------------
admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('permissions',)