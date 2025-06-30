from django.apps import AppConfig


class MonitorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitor'

    def ready(self):
        from .tasks import fetch_machine_data
        if not hasattr(self, 'already_run'):
            fetch_machine_data.delay()
            self.already_run = True
