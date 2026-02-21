from rest_framework import serializers

from .models import Book, Catalog


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "year", "author_name"]


class BookDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title"]


class CatalogSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        error_messages={
            "required": "Catalog name is required.",
            "blank": "Catalog name is required.",
        }
    )

    class Meta:
        model = Catalog
        fields = ["id", "name", "books"]


class CatalogDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ["id", "name"]


class CatalogDetailsSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Catalog
        fields = ["id", "name", "books"]
