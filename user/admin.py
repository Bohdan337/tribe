from django.contrib import admin




from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, UserAdmin)
# admin.site.register(Teacher)
# admin.site.register(ChiefTeacher)
# admin.site.register(Student)