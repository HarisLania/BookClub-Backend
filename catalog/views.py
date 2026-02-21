import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter

from .models import Book, Catalog
from .serializers import (
    BookDropdownSerializer,
    BookSerializer,
    CatalogDetailsSerializer,
    CatalogDropdownSerializer,
    CatalogSerializer,
)

logger = logging.getLogger(__name__)

# Books APIs


class BookListAPIView(generics.ListAPIView):
    """
    Returns full book list with:
    - optional catalog filter (ID)
    - search on title, author_name
    """

    serializer_class = BookSerializer
    queryset = Book.objects.select_related("author").all()

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["catalogs__id"]  # catalog ID only
    search_fields = ["title", "author__name"]


class BookDropdownAPIView(generics.ListAPIView):
    """
    Returns books for frontend dropdown:
    - Only id + title
    - Searchable by title
    """

    serializer_class = BookDropdownSerializer
    queryset = Book.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["title"]


# Catalogs APIs


class CatalogDropdownAPIView(generics.ListAPIView):
    """
    Returns catalogs for frontend dropdown:
    - Only id + name
    - Searchable by name
    """

    serializer_class = CatalogDropdownSerializer
    queryset = Catalog.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class CatalogCreateAPIView(generics.CreateAPIView):
    """
    Create a new catalog
    """

    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer

    def perform_create(self, serializer):
        try:
            catalog = serializer.save()
            logger.info(f"Catalog created (id={catalog.id}, name={catalog.name})")
        except Exception as e:
            logger.exception(
                "Unexpected error while creating catalog: %s",
                e,
            )
            raise


class CatalogManageAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    → retrieve catalog
    PUT    → update catalog
    PATCH  → update catalog
    DELETE → delete catalog
    """

    def get_queryset(self):
        if self.request.method == "GET":
            return Catalog.objects.prefetch_related("books")
        return Catalog.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CatalogDetailsSerializer
        return CatalogSerializer

    def get_object(self):
        try:
            return super().get_object()
        except Exception:
            logger.warning("Catalog not found for given ID")
            raise NotFound(detail="Catalog not found.")

    def perform_update(self, serializer):
        try:
            catalog = serializer.save()
            logger.info(f"Catalog updated (id={catalog.id})")
        except Exception as e:
            logger.exception(
                "Unexpected error while updating catalog: %s",
                e,
            )
            raise

    def perform_destroy(self, instance):
        try:
            instance.delete()
            logger.info(f"Catalog deleted (id={instance.id})")
        except Exception as e:
            logger.exception(
                "Unexpected error while deleting catalog: %s",
                e,
            )
            raise
