from django.contrib import admin

from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):

    list_display = [field.name for field in CustomUser._meta.fields]
    fields = [field.name for field in CustomUser._meta.fields if field.name not in ["id"]]


admin.site.register(CustomUser, CustomUserAdmin)