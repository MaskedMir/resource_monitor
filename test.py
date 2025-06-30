from django.test import TestCase
from django.utils import timezone
from monitor.models import Machine, ResourceData, Incident
from monitor.tasks import check_incidents


class MonitorTests(TestCase):
    def setUp(self):
        self.machine = Machine.objects.create(name="Test Machine", url="http://example.com")

    def test_resource_data_creation(self):
        data = {
            'cpu': 60,
            'mem': '30%',
            'disk': '43%',
            'uptime': '1d 2h 37m 6s'
        }
        resource = ResourceData.objects.create(
            machine=self.machine,
            cpu=data['cpu'],
            mem=data['mem'],
            disk=data['disk'],
            uptime=data['uptime']
        )
        self.assertEqual(resource.cpu, 60)

    def test_incident_creation(self):
        incident = Incident.objects.create(
            machine=self.machine,
            incident_type='cpu',
            threshold='CPU > 85%',
            is_active=True
        )
        self.assertTrue(incident.is_active)

    def test_check_incidents(self):
        # Test CPU incident
        data = {'cpu': 90, 'mem': '30%', 'disk': '43%', 'uptime': '1d'}
        check_incidents(self.machine, data)
        self.assertTrue(Incident.objects.filter(incident_type='cpu').exists())