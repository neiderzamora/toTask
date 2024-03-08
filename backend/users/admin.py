from django.contrib import admin
from users.models import CustomUser, CustomUserManager

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'function', 'function', 'full_name_supervisor', 'full_name_administrator', 'date_joined', 'phone_number', 'birthday_date')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')


admin.site.register(CustomUser, CustomUserAdmin)