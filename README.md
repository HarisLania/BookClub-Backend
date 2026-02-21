# 📚 Book Club API

A clean and well-structured **Django REST Framework** backend for managing **Books** and **Catalogs**.  
This project demonstrates best practices in API design, validation, testing, and project structure.

---

## 🚀 Tech Stack

- Python
- Django
- Django REST Framework
- django-filter
- SQLite (default for local development)
- Ruff (linting)
- Swagger

---

## 📋 Key Features

### 1. Models
- **Book**: Title, Year, Author (ForeignKey)
- **Catalog**: Name (unique), Books (ManyToManyField)
- **Author**: Name

### 2. API Endpoints

#### Catalogs
- `GET /api/catalogs/dropdown/` - List all catalogs
- `POST /api/catalogs/` - Create a new catalog
- `GET /api/catalogs/{id}/` - Retrieve a catalog
- `PUT /api/catalogs/{id}/` - Update a catalog
- `DELETE /api/catalogs/{id}/` - Delete a catalog

#### Books
- `GET /api/books/` - List all books (supports search & catalog filtering)
- `GET /api/books/dropdown/` - List all books for dropdown

### 3. Validation Features
- **Unique Constraints**: Catalog name must be unique
- **Required Fields**: All models have proper validation
- **Custom Error Messages**: User-friendly error responses
- **Search Filtering**: Advanced search on book titles

### 4. Testing
- **Unit Tests**: Comprehensive test suite in `catalog/tests/`

---

## 🛠️ Setup & Installation

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/HarisLania/BookClub-Backend.git
   cd BookClub-Backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate   # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the API**
   - Swagger UI (Interactive Docs): `http://localhost:8000/`
   - OpenAPI Schema (YAML): `http://localhost:8000/schema/`

---

## 🧪 Running Tests

To run the test suite:

```bash
python manage.py test catalog
```

## 📝 API Documentation

### Swagger / OpenAPI

The API exposes an OpenAPI specification along with an interactive Swagger UI.

- **Swagger UI (interactive documentation):**
  - URL: `http://localhost:8000/`
  - Features: Try-it-out requests, request/response examples, schema visualization

- **OpenAPI Schema (YAML):**
  - URL: `http://localhost:8000/schema/`
  - Machine-readable API specification