from django.contrib import admin
from .models import CustomUser

# Register your models here.



admin.site.site_header = "GCash Admin"
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_approved')

admin.site.register(CustomUser, CustomUserAdmin)
