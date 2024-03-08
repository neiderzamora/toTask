from django.contrib import admin
from evidence.models import File, Evidence

class EvidenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'description', 'status', 'date_upload')
    list_filter = ('status', 'task')
    search_fields = ('task', 'description')

class FileAdmin(admin.ModelAdmin):
    list_display = ('archivo','evidence')
    list_filter = ('archivo', 'evidence')
    search_fields = ('archivo', 'evidence')

admin.site.register(Evidence, EvidenceAdmin)
admin.site.register(File, FileAdmin)