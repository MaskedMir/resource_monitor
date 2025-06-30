from .models import Machine, ResourceData, Incident
from datetime import timedelta
from django.db.models import Q
import requests
from celery import shared_task
from django.utils import timezone


@shared_task
def fetch_machine_data():   # Таска сбора информации
    machines = Machine.objects.filter(is_active=True)
    for machine in machines:
        try:
            response = requests.get(machine.url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                ResourceData.objects.create(
                    machine=machine,
                    cpu=data['cpu'],
                    mem=data['mem'],
                    disk=data['disk'],
                    uptime=data['uptime']
                )
                check_incidents(machine, data)
        except requests.RequestException:
            continue


def check_incidents(machine, data):     # Проверка на наличие аномалий(инцидентов)
    now = timezone.now()

    # Проверка CPU
    if data['cpu'] > 85:
        handle_incident(machine, 'cpu', f"CPU usage {data['cpu']}% > 85%")

    # Проверка ОЗУ (если >90% 30 минут)
    if float(data['mem'].strip('%')) > 90:
        last_30_min = now - timedelta(minutes=30)
        mem_data = ResourceData.objects.filter(
            machine=machine,
            timestamp__gte=last_30_min
        ).order_by('timestamp')

        if all(float(d.mem.strip('%')) > 90 for d in mem_data):
            handle_incident(machine, 'mem', f"Memory usage {data['mem']} > 90% for 30 minutes")

    # Проверка диска (если >95% 2 часа)
    if float(data['disk'].strip('%')) > 95:
        last_2_hours = now - timedelta(hours=2)
        disk_data = ResourceData.objects.filter(
            machine=machine,
            timestamp__gte=last_2_hours
        ).order_by('timestamp')

        if all(float(d.disk.strip('%')) > 95 for d in disk_data):
            handle_incident(machine, 'disk', f"Disk usage {data['disk']} > 95% for 2 hours")


def handle_incident(machine, incident_type, threshold):     # Запись инцидента
    # Проверка, не происходит ли уже какой-то подобный инцидент
    existing = Incident.objects.filter(
        machine=machine,
        incident_type=incident_type,
        is_active=True
    ).first()

    if not existing:
        Incident.objects.create(
            machine=machine,
            incident_type=incident_type,
            threshold=threshold,
            is_active=True
        )