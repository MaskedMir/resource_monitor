from django.db import models
from django.contrib.auth.models import User


class Machine(models.Model):    # Машина - сервер с которого собираем данные
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ResourceData(models.Model):   # Статистика, которую собираем
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu = models.FloatField()
    mem = models.CharField(max_length=10)
    disk = models.CharField(max_length=10)
    uptime = models.CharField(max_length=50)

    class Meta:
        ordering = ['-timestamp']


class Incident(models.Model):   # Инциденты и что сохраняем
    INCIDENT_TYPES = (
        ('cpu', 'High CPU Usage'),
        ('mem', 'High Memory Usage'),
        ('disk', 'High Disk Usage'),
    )

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    incident_type = models.CharField(max_length=10, choices=INCIDENT_TYPES)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    threshold = models.CharField(max_length=100)
    resolved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.machine.name} - {self.get_incident_type_display()}"

    class Meta:
        ordering = ['-start_time']