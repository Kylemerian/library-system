import unittest
import os
import json
from models.library import Library
from models.book import Book


class TestLibrary(unittest.TestCase):
    TEST_DATA_FILE = "test_data.json"
        
    """
    Тесты для Library
    """
    def setUp(self):
        """
        Подготовка перед каждым тестом
        """
        self.library = Library(data_file=self.TEST_DATA_FILE)
        self.library.books = []
        self.library.save_data()

    def tearDown(self):
        """
        Очистка после каждого теста
        """
        if os.path.exists(self.TEST_DATA_FILE):
            os.remove(self.TEST_DATA_FILE)

    def test_add_book(self):
        """
        Тест добавления книги
        """
        self.library.add_book("Book Test", "Author Name", 2023)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Book Test")
        self.assertEqual(self.library.books[0].status, "в наличии")

    def test_remove_book(self):
        """
        Тест удаления книги
        """
        self.library.add_book("Book Test", "Author Name", 2023)
        book_id = self.library.books[0].id
        self.library.remove_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_remove_nonexistent_book(self):
        """
        Тест попытки удаления несуществующей книги
        """
        self.library.add_book("Book Test", "Author Name", 2023)
        initial_count = len(self.library.books)
        self.library.remove_book(999)
        self.assertEqual(len(self.library.books), initial_count)

    def test_search_books(self):
        """
        Тест поиска книг
        """
        self.library.add_book("Python qwe", "Author A", 2021)
        self.library.add_book("123 Python", "Author B", 2022)
        self.library.add_book("qwe123 Python", "Author C", 2023)

        results = self.library.search_books("Python")
        self.assertEqual(len(results), 3)

        results = self.library.search_books("Author B")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Author B")

        results = self.library.search_books("2023")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].year, 2023)

    def test_display_books(self):
        """
        Тест отображения книг
        """
        self.library.add_book("Book 1", "Author 1", 2021)
        self.library.add_book("Book 2", "Author 2", 2022)
        self.assertEqual(len(self.library.books), 2)

        book_list = [str(book) for book in self.library.books]
        self.assertIn("Book 1", book_list[0])
        self.assertIn("Author 1", book_list[0])
        self.assertIn("Book 2", book_list[1])
        self.assertIn("Author 2", book_list[1])

    def test_update_status(self):
        """
        Тест обновления статуса книги
        """
        self.library.add_book("Book Test", "Author Name", 2023)
        book_id = self.library.books[0].id
        self.library.update_status(book_id, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

        self.library.update_status(book_id, "в наличии")
        self.assertEqual(self.library.books[0].status, "в наличии")

    def test_update_status_invalid(self):
        """
        Тест обновления статуса с некорректным значением
        """
        self.library.add_book("Book Test", "Author Name", 2023)
        book_id = self.library.books[0].id
        self.library.update_status(book_id, "недоступно")
        self.assertEqual(self.library.books[0].status, "в наличии")

    def test_save_and_load_data(self):
        """
        Тест сохранения и загрузки данных
        """
        self.library.add_book("Test Book", "Author Name", 2024)
        self.library.save_data()

        new_library = Library(data_file=self.TEST_DATA_FILE)
        self.assertEqual(len(new_library.books), 1)
        self.assertEqual(new_library.books[0].title, "Test Book")

if __name__ == "__main__":
    unittest.main()