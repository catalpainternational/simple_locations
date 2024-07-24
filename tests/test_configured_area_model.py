from django.test import TestCase

from simple_locations.models import Area, AREA_MODEL_LABEL
from tests.factories import AreaFactory


class ConfiguredModelTestCase(TestCase):
    ''' Test overriding the configured Area model\
        run tests with `TEST_CONFIGURED_AREA_MODEL=1 ./manage.py test` to run the whole test suite
        using the sl_tests.ConfiguredAreaModel model, which has an extra field or two
        tests should still all pass without TEST_CONFIGURED_AREA_MODEL checking default behaviour still applies
    '''
    @classmethod
    def setUpTestData(cls):
        cls.area = AreaFactory()

    def test_stuff(self):
        self.assertEqual(Area.objects.count(), 1)

        area = Area.objects.first()
        if AREA_MODEL_LABEL == 'sl_tests.ConfiguredAreaModel':
            self.assertTrue(hasattr(area, "extra_field"))
