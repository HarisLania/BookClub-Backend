from rest_framework import serializers
from rest_framework.validators import UniqueValidator

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
        validators=[
            UniqueValidator(
                queryset=Catalog.objects.all(),
                message="A catalog with this name already exists.",
            )
        ],
        error_messages={
            "required": "Catalog name is required.",
            "blank": "Catalog name cannot be empty.",
        },
    )

    books = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        queryset=Book.objects.all(),
        error_messages={
            "does_not_exist": "One or more book IDs are invalid.",
            "incorrect_type": "Books must be provided as a list of IDs.",
        },
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
