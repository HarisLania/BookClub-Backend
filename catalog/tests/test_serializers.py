from django.test import TestCase

from catalog.models import Catalog
from catalog.serializers import CatalogSerializer


class TestCatalogSerializer(TestCase):
    def test_catalog_name_required(self):
        serializer = CatalogSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertEqual(serializer.errors["name"][0], "Catalog name is required.")

    def test_catalog_name_unique(self):
        Catalog.objects.create(name="Tech")

        serializer = CatalogSerializer(data={"name": "Tech"})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["name"][0], "A catalog with this name already exists."
        )

    def test_invalid_book_ids(self):
        serializer = CatalogSerializer(data={"name": "Science", "books": [999]})
        self.assertFalse(serializer.is_valid())
        self.assertIn("books", serializer.errors)
