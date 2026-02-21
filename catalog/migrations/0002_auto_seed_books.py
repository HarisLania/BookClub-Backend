from django.db import migrations

def seed_books_and_authors(apps, schema_editor):
    Author = apps.get_model('catalog', 'Author')
    Book = apps.get_model('catalog', 'Book')

    initial_books = [
        {"title": "Dune", "year": 1965, "author": "Frank Herbert"},
        {"title": "Ender's Game", "year": 1985, "author": "Orson Scott Card"},
        {"title": "1984", "year": 1949, "author": "George Orwell"},
        {"title": "Fahrenheit 451", "year": 1953, "author": "Ray Bradbury"},
        {"title": "Brave New World", "year": 1932, "author": "Aldous Huxley"},
    ]

    for book_data in initial_books:
        author, _ = Author.objects.get_or_create(name=book_data['author'])
        Book.objects.get_or_create(title=book_data['title'], year=book_data['year'], author=author)

class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),  # your initial migration with tables
    ]

    operations = [
        migrations.RunPython(seed_books_and_authors),
    ]