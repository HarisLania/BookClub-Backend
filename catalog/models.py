from django.db import models
from django.db.utils import IntegrityError


class Author(models.Model):
    """
    Represents an Author.
    """

    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create(cls, name: str):
        """
        Safely get or create an author.
        """
        try:
            author, created = cls.objects.get_or_create(name=name)
            return author, created
        except IntegrityError:
            return cls.objects.get(name=name), False


class Book(models.Model):
    """
    Represents a Book entity.
    """

    title = models.CharField(max_length=255, unique=True)
    year = models.PositiveIntegerField()
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="books")

    class Meta:
        ordering = ["title"]
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return f"{self.title} ({self.year}) by {self.author.name}"

    @classmethod
    def get_or_create(cls, title: str, year: int, author_name: str):
        """
        Safely get or create a book by title, linking to author.
        """
        author, _ = Author.get_or_create(author_name)
        try:
            book, created = cls.objects.get_or_create(
                title=title, defaults={"year": year, "author": author}
            )
            return book, created
        except IntegrityError:
            return cls.objects.get(title=title), False


class Catalog(models.Model):
    """
    Represents a Catalog containing multiple books.
    """

    name = models.CharField(max_length=255, unique=True)
    books = models.ManyToManyField(Book, related_name="catalogs", blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Catalog"
        verbose_name_plural = "Catalogs"

    def __str__(self):
        return self.name
