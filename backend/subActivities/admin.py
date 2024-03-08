from django.contrib import admin
from subActivities.models import SubActivities

class SubActivitiesAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'user', 'activity', 'percentage', 'status', 'assigned_resources', 'date_start', 'date_finish', 'date_created')
    list_filter = ('status', 'name')
    search_fields = ('name', 'description')

admin.site.register(SubActivities, SubActivitiesAdmin)