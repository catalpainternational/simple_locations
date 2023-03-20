from django.test import Client, TestCase
from django.urls import reverse

from tests.factories import AreaFactory


class SimpleLocationsAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        a = AreaFactory()

        self.area_list_url = (reverse("api-1.0.0:area_list"))
        self.area_type_list_url = reverse("api-1.0.0:area_type_list")
        self.area_id_url = reverse("api-1.0.0:area_id", kwargs={"area_id": a.id})
        self.area_children_url = reverse("api-1.0.0:area_children", kwargs={"area_id": a.id})
        self.area_type_url = reverse("api-1.0.0:area_type", kwargs={"area_type": a.kind.slug})
        self.area_children_compressed_url = reverse("api-1.0.0:area_children_compressed", kwargs={"area_id": a.id, "simplify": 3, "quantize": 3})
        self.area_type_compressed_url = reverse("api-1.0.0:area_type_compressed", kwargs={"area_type": a.kind.slug, "simplify": 3, "quantize": 3})


    def test_area_list(self):
        response = self.client.get(self.area_list_url)
        self.assertEqual(response.status_code, 200)

    def test_areatype_list(self):
        response = self.client.get(self.area_type_list_url)
        self.assertEqual(response.status_code, 200)

    def test_area_by_id(self):
        response = self.client.get(self.area_id_url)
        self.assertEqual(response.status_code, 200)

    def test_area_by_parent(self):
        response = self.client.get(self.area_children_url)
        self.assertEqual(response.status_code, 200)

    def test_area_by_type(self):
        response = self.client.get(self.area_type_url)
        self.assertEqual(response.status_code, 200)

    def test_area_children_compressed(self):
        response = self.client.get(self.area_children_compressed_url)    
        self.assertEqual(response.status_code, 200)

    def test_area_type_compressed(self):
        response = self.client.get(self.area_type_compressed_url)    
        self.assertEqual(response.status_code, 200)


