from django.contrib import admin
from base.models import Activities

class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'user', 'status', 'assigned_resources', 'date_start', 'date_finish', 'date_created')
    list_filter = ('status', 'name')
    search_fields = ('name', 'description')

admin.site.register(Activities, ActivitiesAdmin)