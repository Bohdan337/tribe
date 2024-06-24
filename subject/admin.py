from django.contrib import admin
from .models import Subject, Material, MaterialFile, Grade


admin.site.register(Subject)
admin.site.register(Material)
admin.site.register(MaterialFile)
admin.site.register(Grade)


