import pytest
from src.library_books.errors import CatalogError
from src.library_books.classes import Catalog
from src.library_books.classes import Book

def test_available_object():
    book = Book("978-5-97060-848-7", "Мартин Фаулер", "Рефакторинг кода: улучшение проекта существующего кода", "Разработка ПО", 2020, "ДМК Пресс")
    assert book.id == "978-5-97060-848-7"

def test_empty_value():
    with pytest.raises(CatalogError) as e:
        Book("978-5-97060-848-7", "", "Рефакторинг кода: улучшение проекта существующего кода", "Разработка ПО", 2020, "ДМК Пресс")
    assert str(e.value) == "Wrong format"

def test_unavailable_year():
    with pytest.raises(CatalogError) as e:
        Book("978-5-97060-848-7", "Мартин Фаулер", "Рефакторинг кода: улучшение проекта существующего кода", "Разработка ПО", 2046, "ДМК Пресс")
    assert str(e.value) == "Wrong format"

def test_unavailable_id():
    with pytest.raises(CatalogError) as e:
        Book("978-5-97060-848-8", "Мартин Фаулер", "Рефакторинг кода: улучшение проекта существующего кода", "Разработка ПО", 2020, "ДМК Пресс")
    assert str(e.value) == "Wrong format"

def test_add():
    catalog = Catalog("src/library_books/library.json")
    book = Book("978-5-97060-848-7", "Мартин Фаулер", "Рефакторинг кода: улучшение проекта существующего кода", "Разработка ПО", 2020, "ДМК Пресс")
    catalog.add(book)
    assert book in catalog

def test_get():
    catalog = Catalog("src/library_books/library.json")
    assert catalog.get("978-5-97060-668-1").id == "978-5-97060-668-1"

def test_remove():
    catalog = Catalog("src/library_books/library.json")
    book = catalog.get("978-5-97060-668-1")
    catalog.remove("978-5-97060-668-1")
    assert book not in catalog

def test_id_exists():
    catalog = Catalog("src/library_books/library.json")
    book = Book("978-5-97060-668-1", "Марк Лутц", "Изучаем Python", "Программирование", 2019, "ДМК Пресс")
    with pytest.raises(CatalogError) as e:
        catalog.add(book)
    assert str(e.value) == "ID already exists"

def test_find_by_category():
    catalog = Catalog("src/library_books/library.json")
    assert all([book.category == "Художественная литература" for book in catalog.find_by_category("Художественная литература")])

def test_find_by_name():
    catalog = Catalog("src/library_books/library.json")
    assert [book for book in catalog.find_by_name("иллюстрированное")][0].id == "978-5-4461-1734-5"

def test_iter():
    catalog = Catalog("src/library_books/library.json")
    books = [book for book in catalog]
    assert books[0].name == "1984" and books[-1].name == "Чистый код: создание, анализ и рефакторинг"

def test_roundtrip():
    catalog = Catalog("src/library_books/library.json")
    books = [book for book in catalog]
    catalog.save()
    catalog.load()
    new_books = [book for book in catalog]
    assert books == new_books

def test_broken_file():
    with open("src/library_books/library.json", "w", encoding='utf-8') as f:
        f.write('{"format_version":1,"items":{"978-5-97060-668-1":{"id":"978-5-97060-668-1","author":"Марк Лутц","name":"Изучаем Python","category":"Программирование","year":2019,"publisher":"ДМК Пресс"},"978-5-4461-1258-6":{"id":"978-5-4461-1258-6","author":"Эрик Мэтиз","name":"Изучаем Python. Программирование лифтов, гитар и всего остального","category":"Программирование","year":2020,"publisher":"Питер"},"978-5-4461-1521-1":{"id":"978-5-4461-1521-1","author":"Роберт Мартин","name":"Чистый код: создание, анализ и рефакторинг","category":"Разработка ПО","year":2021,"publisher":"Питер"},"978-5-17-118366-0":{"id":"978-5-17-118366-0","author":"Джордж Оруэлл","name":"1984","category":"Художественная литература","year":2019,"publisher":"АСТ"},"978-5-4461-1734-5":{"id":"978-5-4461-1734-5","author":"Адитья Бхаргава","name":"Грокаем алгоритмы. Иллюстрированное пособие для программистов","category":"Алгоритмы","year":2021,"publisher":"Питер"},"978-5-907458-15-4":{"id":"978-5-907458-15-4","author":"Рэй Брэдбери","name":"451 градус по Фаренгейту","category":"Художественная литература","year":2022,"publisher":"Эксмо"}}')
    with pytest.raises(CatalogError) as e:
        Catalog("src/library_books/library.json")
    with open("src/library_books/library.json", "w", encoding='utf-8') as f:
        f.write('{"format_version":1,"items":{"978-5-97060-668-1":{"id":"978-5-97060-668-1","author":"Марк Лутц","name":"Изучаем Python","category":"Программирование","year":2019,"publisher":"ДМК Пресс"},"978-5-4461-1258-6":{"id":"978-5-4461-1258-6","author":"Эрик Мэтиз","name":"Изучаем Python. Программирование лифтов, гитар и всего остального","category":"Программирование","year":2020,"publisher":"Питер"},"978-5-4461-1521-1":{"id":"978-5-4461-1521-1","author":"Роберт Мартин","name":"Чистый код: создание, анализ и рефакторинг","category":"Разработка ПО","year":2021,"publisher":"Питер"},"978-5-17-118366-0":{"id":"978-5-17-118366-0","author":"Джордж Оруэлл","name":"1984","category":"Художественная литература","year":2019,"publisher":"АСТ"},"978-5-4461-1734-5":{"id":"978-5-4461-1734-5","author":"Адитья Бхаргава","name":"Грокаем алгоритмы. Иллюстрированное пособие для программистов","category":"Алгоритмы","year":2021,"publisher":"Питер"},"978-5-907458-15-4":{"id":"978-5-907458-15-4","author":"Рэй Брэдбери","name":"451 градус по Фаренгейту","category":"Художественная литература","year":2022,"publisher":"Эксмо"}}}')
    assert str(e.value) == "Wrong File"

def test_unknown_format():
    with open("src/library_books/library.json", "w", encoding='utf-8') as f:
        f.write('{"format_version":2,"items":{"978-5-97060-668-1":{"id":"978-5-97060-668-1","author":"Марк Лутц","name":"Изучаем Python","category":"Программирование","year":2019,"publisher":"ДМК Пресс"},"978-5-4461-1258-6":{"id":"978-5-4461-1258-6","author":"Эрик Мэтиз","name":"Изучаем Python. Программирование лифтов, гитар и всего остального","category":"Программирование","year":2020,"publisher":"Питер"},"978-5-4461-1521-1":{"id":"978-5-4461-1521-1","author":"Роберт Мартин","name":"Чистый код: создание, анализ и рефакторинг","category":"Разработка ПО","year":2021,"publisher":"Питер"},"978-5-17-118366-0":{"id":"978-5-17-118366-0","author":"Джордж Оруэлл","name":"1984","category":"Художественная литература","year":2019,"publisher":"АСТ"},"978-5-4461-1734-5":{"id":"978-5-4461-1734-5","author":"Адитья Бхаргава","name":"Грокаем алгоритмы. Иллюстрированное пособие для программистов","category":"Алгоритмы","year":2021,"publisher":"Питер"},"978-5-907458-15-4":{"id":"978-5-907458-15-4","author":"Рэй Брэдбери","name":"451 градус по Фаренгейту","category":"Художественная литература","year":2022,"publisher":"Эксмо"}}}')
    with pytest.raises(CatalogError) as e:
        Catalog("src/library_books/unknown_format_library.json")
    with open("src/library_books/library.json", "w", encoding='utf-8') as f:
        f.write('{"format_version":1,"items":{"978-5-97060-668-1":{"id":"978-5-97060-668-1","author":"Марк Лутц","name":"Изучаем Python","category":"Программирование","year":2019,"publisher":"ДМК Пресс"},"978-5-4461-1258-6":{"id":"978-5-4461-1258-6","author":"Эрик Мэтиз","name":"Изучаем Python. Программирование лифтов, гитар и всего остального","category":"Программирование","year":2020,"publisher":"Питер"},"978-5-4461-1521-1":{"id":"978-5-4461-1521-1","author":"Роберт Мартин","name":"Чистый код: создание, анализ и рефакторинг","category":"Разработка ПО","year":2021,"publisher":"Питер"},"978-5-17-118366-0":{"id":"978-5-17-118366-0","author":"Джордж Оруэлл","name":"1984","category":"Художественная литература","year":2019,"publisher":"АСТ"},"978-5-4461-1734-5":{"id":"978-5-4461-1734-5","author":"Адитья Бхаргава","name":"Грокаем алгоритмы. Иллюстрированное пособие для программистов","category":"Алгоритмы","year":2021,"publisher":"Питер"},"978-5-907458-15-4":{"id":"978-5-907458-15-4","author":"Рэй Брэдбери","name":"451 градус по Фаренгейту","category":"Художественная литература","year":2022,"publisher":"Эксмо"}}}')
    assert str(e.value) == "Wrong File"

def test_load_error():
    catalog = Catalog("src/library_books/library.json")
    books = [book for book in catalog]
    with open("src/library_books/library.json", "w", encoding='utf-8') as f:
        f.write('{"format_version":1,"items":{"978-5-97060-668-1":{"id":"978-5-97060-668-1","author":"Марк Лутц","name":"Изучаем Python","category":"Программирование","year":2019,"publisher":"ДМК Пресс"},"978-5-4461-1258-6":{"id":"978-5-4461-1258-6","author":"Эрик Мэтиз","name":"Изучаем Python. Программирование лифтов, гитар и всего остального","category":"Программирование","year":2020,"publisher":"Питер"},"978-5-4461-1521-1":{"id":"978-5-4461-1521-1","author":"Роберт Мартин","name":"Чистый код: создание, анализ и рефакторинг","category":"Разработка ПО","year":2021,"publisher":"Питер"},"978-5-17-118366-0":{"id":"978-5-17-118366-0","author":"Джордж Оруэлл","name":"1984","category":"Художественная литература","year":2019,"publisher":"АСТ"},"978-5-4461-1734-5":{"id":"978-5-4461-1734-5","author":"Адитья Бхаргава","name":"Грокаем алгоритмы. Иллюстрированное пособие для программистов","category":"Алгоритмы","year":2021,"publisher":"Питер"},"978-5-907458-15-4":{"id":"978-5-907458-15-4","author":"Рэй Брэдбери","name":"451 градус по Фаренгейту","category":"Художественная литература","year":2022,"publisher":"Эксмо"}}')
    try:
        catalog.load()
    except Exception:
        with open("src/library_books/library.json", "w", encoding='utf-8') as f:
            f.write('{"format_version":1,"items":{"978-5-97060-668-1":{"id":"978-5-97060-668-1","author":"Марк Лутц","name":"Изучаем Python","category":"Программирование","year":2019,"publisher":"ДМК Пресс"},"978-5-4461-1258-6":{"id":"978-5-4461-1258-6","author":"Эрик Мэтиз","name":"Изучаем Python. Программирование лифтов, гитар и всего остального","category":"Программирование","year":2020,"publisher":"Питер"},"978-5-4461-1521-1":{"id":"978-5-4461-1521-1","author":"Роберт Мартин","name":"Чистый код: создание, анализ и рефакторинг","category":"Разработка ПО","year":2021,"publisher":"Питер"},"978-5-17-118366-0":{"id":"978-5-17-118366-0","author":"Джордж Оруэлл","name":"1984","category":"Художественная литература","year":2019,"publisher":"АСТ"},"978-5-4461-1734-5":{"id":"978-5-4461-1734-5","author":"Адитья Бхаргава","name":"Грокаем алгоритмы. Иллюстрированное пособие для программистов","category":"Алгоритмы","year":2021,"publisher":"Питер"},"978-5-907458-15-4":{"id":"978-5-907458-15-4","author":"Рэй Брэдбери","name":"451 градус по Фаренгейту","category":"Художественная литература","year":2022,"publisher":"Эксмо"}}}')
    new_books = [book for book in catalog]
    assert books == new_books
