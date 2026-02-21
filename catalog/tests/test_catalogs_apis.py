from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Catalog


class TestCatalogCreateAPIView(APITestCase):
    def setUp(self):
        self.url = reverse("catalog-create")

    def test_create_catalog_success(self):
        payload = {"name": "Programming"}

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Catalog.objects.count(), 1)
        self.assertEqual(Catalog.objects.first().name, "Programming")

    def test_create_catalog_duplicate_name(self):
        Catalog.objects.create(name="Programming")

        payload = {"name": "Programming"}

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_create_catalog_empty_payload(self):
        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_create_catalog_invalid_books_type(self):
        payload = {"name": "Tech", "books": "not-a-list"}

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("books", response.data)


class TestCatalogManageAPIView(APITestCase):
    def test_get_invalid_catalog_id(self):
        url = reverse("catalog-manage", args=[9999])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Catalog not found.")

    def test_get_catalog_success(self):
        catalog = Catalog.objects.create(name="Programming")

        url = reverse("catalog-manage", args=[catalog.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], catalog.id)
        self.assertEqual(response.data["name"], "Programming")
        self.assertIn("books", response.data)

    def test_update_catalog_success(self):
        catalog = Catalog.objects.create(name="Science")

        url = reverse("catalog-manage", args=[catalog.id])

        response = self.client.put(url, {"name": "Data Science"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Data Science")

        catalog.refresh_from_db()
        self.assertEqual(catalog.name, "Data Science")

    def test_delete_catalog_success(self):
        catalog = Catalog.objects.create(name="Temp")

        url = reverse("catalog-manage", args=[catalog.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Catalog.objects.filter(id=catalog.id).exists())

    def test_update_catalog_duplicate_name(self):
        Catalog.objects.create(name="Tech")
        cat2 = Catalog.objects.create(name="Science")

        url = reverse("catalog-manage", args=[cat2.id])

        response = self.client.put(url, {"name": "Tech"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
