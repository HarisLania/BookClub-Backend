from django.urls import path

from .views import (
    BookDropdownAPIView,
    BookListAPIView,
    CatalogCreateAPIView,
    CatalogDropdownAPIView,
    CatalogManageAPIView,
)

urlpatterns = [
    # Books
    path("books/", BookListAPIView.as_view(), name="book-list"),
    path("books/dropdown/", BookDropdownAPIView.as_view(), name="book-dropdown"),
    # Catalogs
    path(
        "catalogs/dropdown/", CatalogDropdownAPIView.as_view(), name="catalog-dropdown"
    ),
    path("catalogs/", CatalogCreateAPIView.as_view(), name="catalog-create"),
    path("catalogs/<int:pk>/", CatalogManageAPIView.as_view(), name="catalog-manage"),
]
