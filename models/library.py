from typing import List
from .book import Book
import json

DATA_FILE = "save.json"

class Library:
    """
    Класс для управления библиотекой
    """

    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.books = self.load_data()

    def load_data(self) -> List[Book]:
        """
        Загружает данные из файла
        """
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                books_data = json.load(file)
                return [Book(**book) for book in books_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []


    def save_data(self) -> None:
        """
        Сохраняет данные в файл
        """
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump([book.__dict__ for book in self.books], file, ensure_ascii=False, indent=4)


    def add_book(self, title: str, author: str, year: int) -> None:
        """
        Добавляет книгу в библиотеку
        """
        book_id = max([book.id for book in self.books], default=0) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_data()
        print(f"Книга добавлена: {new_book}")


    def remove_book(self, book_id: int) -> None:
        """
        Удаляет книгу из библиотеки по ID
        """
        original_count = len(self.books)
        self.books = [book for book in self.books if book.id != book_id]
        if len(self.books) == original_count:
            print(f"Книга с ID {book_id} не найдена.")
        else:
            self.save_data()
            print(f"Книга с ID {book_id} удалена.")


    def search_books(self, keyword: str) -> List[Book]:
        """
        Ищет книги по ключевому слову в названии, авторе или году
        """
        return [
            book
            for book in self.books
            if keyword.lower() in book.title.lower()
            or keyword.lower() in book.author.lower()
            or keyword == str(book.year)
        ]


    def display_books(self) -> None:
        """
        Выводит все книги в библиотеке
        """
        if not self.books:
            print("Библиотека пуста.")
        else:
            for book in self.books:
                print(book)


    def update_status(self, book_id: int, status: str) -> None:
        """
        Изменяет статус книги по ID
        """
        if status not in ["в наличии", "выдана"]:
            print("Некорректный статус. Допустимые значения: 'в наличии', 'выдана'.")
            return
        for book in self.books:
            if book.id == book_id:
                book.status = status
                self.save_data()
                print(f"Статус книги с ID {book_id} обновлен на '{status}'.")
                return
        print(f"Книга с ID {book_id} не найдена.")