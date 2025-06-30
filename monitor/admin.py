from celery.utils.time import timezone
from django.contrib import admin
from .models import Machine, ResourceData, Incident


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'url')


@admin.register(ResourceData)
class ResourceDataAdmin(admin.ModelAdmin):
    list_display = ('machine', 'timestamp', 'cpu', 'mem', 'disk')
    list_filter = ('machine',)
    date_hierarchy = 'timestamp'


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('machine', 'incident_type', 'start_time', 'end_time', 'is_active')
    list_filter = ('incident_type', 'is_active', 'machine')
    date_hierarchy = 'start_time'
    actions = ['resolve_incidents']

    def resolve_incidents(self, request, queryset):
        queryset.update(is_active=False, end_time=timezone.now(), resolved_by=request.user)

    resolve_incidents.short_description = "Mark selected incidents as resolved"
