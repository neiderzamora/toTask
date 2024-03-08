from django.contrib import admin
from tasks.models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'user', 'user_staff', 'subActivity', 'percentage', 'status', 'assigned_resources', 'date_start', 'date_finish', 'date_created')
    list_filter = ('status', 'name')
    search_fields = ('name', 'description')  

admin.site.register(Task, TaskAdmin)