from celery.utils.time import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Incident
from django.http import JsonResponse

# Обработка страницы входа
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('incidents')
    return render(request, 'monitor/login.html')

# Выход из системы
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Страница с инцидентами
@login_required
def incidents_view(request):
    return render(request, 'monitor/incidents.html')

# Получение данных об инцидентах для таблицы
@login_required
def get_incidents(request):
    incidents = Incident.objects.all().order_by('-start_time')

    # Формируем удобный JSON для JavaScript
    data = [{
        'id': i.id,
        'machine': i.machine.name,
        'type': i.get_incident_type_display(),
        'start_time': i.start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': i.end_time.strftime('%Y-%m-%d %H:%M:%S') if i.end_time else None,
        'is_active': i.is_active,
        'threshold': i.threshold,
        'resolved_by': i.resolved_by.username if i.resolved_by else None
    } for i in incidents]
    return JsonResponse({'incidents': data})

# Закрытие инцидента
@login_required
def resolve_incident(request, incident_id):
    if request.method == 'POST':
        incident = Incident.objects.get(id=incident_id)
        incident.is_active = False
        incident.end_time = timezone.now()
        incident.resolved_by = request.user
        incident.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
