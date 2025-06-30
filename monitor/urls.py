from django.urls import path
from . import views

urlpatterns = [
    # Страница входа в систему
    path('login/', views.login_view, name='login'),

    # Выход из системы (разлогинивание)
    path('logout/', views.logout_view, name='logout'),

    # Основная страница с таблицей инцидентов
    path('incidents/', views.incidents_view, name='incidents'),

    # API endpoint для получения данных об инцидентах (JSON)
    path('api/incidents/', views.get_incidents, name='get_incidents'),

     # API endpoint для отметки инцидента как решенного
    path('api/incidents/<int:incident_id>/resolve/', views.resolve_incident, name='resolve_incident'),      #
]