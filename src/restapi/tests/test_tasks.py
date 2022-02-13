from django.test import TestCase, override_settings
from restapi.tasks import periodic_companies_maintenance


class TasksTestCase(TestCase):
    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_periodic_companies_maintenance_has_success(self):
        self.assertTrue(periodic_companies_maintenance.delay())
