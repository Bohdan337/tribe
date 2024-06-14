from django.contrib import admin




from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from .models import Profile

# The class `UserAdmin` defines fieldsets for adding and displaying user information in an admin
# interface.


class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_student', 'is_teacher'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'surname', 'email', 'is_student', 'is_teacher', 'is_chief_teacher')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Profile)