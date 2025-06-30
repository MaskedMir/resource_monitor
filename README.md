# resource_monitor

# Resource Monitor System

Простая система мониторинга ресурсов серверов на Django + Celery

## 🚀 Быстрый старт

1. **Клонируйте репозиторий**
```bash
git clone https://github.com/MaskedMir/resource_monitor.git
cd resource_monitor
```

2. **Установите зависимости**
```bash
pip install -r requirements.txt
```

3. **Настройте базу данных**  
Отредактируйте `resource_monitor/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'resource_monitor',
        'USER': 'ваш_пользователь',
        'PASSWORD': 'ваш_пароль',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

4. **Примените миграции**
```bash
python manage.py migrate
```

5. **Создайте суперпользователя**
```bash
python manage.py createsuperuser
```

6. **Запустите Redis**  
(Должен быть установлен и запущен на localhost:6379)

7. **Запустите сервисы**  
В разных терминалах:
```bash
# Celery worker
celery -A resource_monitor worker --pool=solo --loglevel=info

# Celery beat (для периодических задач)
celery -A resource_monitor beat --loglevel=info

# Django сервер
python manage.py runserver
```

8. **Добавьте тестовые серверы**  
Через админку (`/admin`) или Django shell:
```python
from monitor.models import Machine
Machine.objects.create(name="Test Server", url="http://example.com/mock-endpoint")
```

## 🔍 Доступ
- Веб-интерфейс: `http://localhost:8000`
- Админка: `http://localhost:8000/admin`

## ⚙️ Как работает
- Каждые 15 минут Celery опрашивает все серверы
- При превышении лимитов создаются инциденты
- Интерфейс автоматически обновляет список инцидентов


P.s. README написан нейронкой ;)
