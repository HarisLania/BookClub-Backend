from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Author, Book, Catalog


class TestBookListAPIView(APITestCase):
    def setUp(self):
        self.author_1 = Author.objects.create(name="Robert Martin")
        self.author_2 = Author.objects.create(name="Cal Newport")

        self.book_1 = Book.objects.create(
            title="Clean Code", year=1990, author=self.author_1
        )
        self.book_2 = Book.objects.create(
            title="Deep Work", year=2000, author=self.author_2
        )

        self.catalog = Catalog.objects.create(name="Programming")
        self.catalog.books.add(self.book_1)

        self.url = reverse("book-list")

    def test_search_by_title(self):
        response = self.client.get(self.url, {"search": "Clean"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Clean Code")

    def test_search_by_author(self):
        response = self.client.get(self.url, {"search": "Newport"})

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Deep Work")

    def test_filter_by_catalog(self):
        response = self.client.get(self.url, {"catalogs__id": self.catalog.id})

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Clean Code")

    def test_search_with_catalog_filter(self):
        response = self.client.get(
            self.url, {"search": "Clean", "catalogs__id": self.catalog.id}
        )

        self.assertEqual(len(response.data), 1)

    def test_search_not_in_catalog_returns_empty(self):
        response = self.client.get(
            self.url, {"search": "Deep", "catalogs__id": self.catalog.id}
        )

        self.assertEqual(len(response.data), 0)
