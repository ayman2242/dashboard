from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    nni = models.CharField(max_length=20, blank=True, null=True, verbose_name="National ID")
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",    
        related_query_name="customuser",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",   
        related_query_name="customuser",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class School(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True, null=True)
    wilaya = models.CharField(max_length=50, blank=True, null=True)
    moughatta = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DirectorAuthorization(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='director_auth')
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    diploma = models.CharField(max_length=100, blank=True, null=True)
    authorization_number = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    qr_code = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.school.name}"

class TeacherAuthorization(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_auth')
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=50)
    diploma = models.CharField(max_length=100, blank=True, null=True)
    authorization_number = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    qr_code = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialty}"