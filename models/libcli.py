from models.library import *

class LibraryCLI:
    """
    Класс для взаимодействия с пользователем через консоль
    """

    def __init__(self):
        self.library = Library()
        self.commands = {
            "add": self.add_book,
            "remove": self.remove_book,
            "search": self.search_books,
            "display": self.display_books,
            "update": self.update_status,
            "exit": self.exit_program,
        }
        self.running = True


    def run(self) -> None:
        """
        Запускает CLI интерфейс
        """
        print("Система управления библиотекой")
        while self.running:
            print("\nКоманды:")
            print("1. add - Добавить книгу")
            print("2. remove - Удалить книгу")
            print("3. search - Найти книгу")
            print("4. display - Показать все книги")
            print("5. update - Изменить статус книги")
            print("6. exit - Выйти из программы")

            command = input("Введите команду: ").strip().lower()
            action = self.commands.get(command)
            if action:
                action()
            else:
                print("Неизвестная команда. Попробуйте снова.")


    def add_book(self) -> None:
        """
        Добавление книги
        """
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        try:
            year = int(input("Введите год издания книги: "))
            self.library.add_book(title, author, year)
        except ValueError:
            print("Год издания должен быть числом.")


    def remove_book(self) -> None:
        """
        Удаление книги
        """
        try:
            book_id = int(input("Введите ID книги для удаления: "))
            self.library.remove_book(book_id)
        except ValueError:
            print("ID должен быть числом.")


    def search_books(self) -> None:
        """
        Поиск книг
        """
        keyword = input("Введите ключевое слово для поиска: ")
        results = self.library.search_books(keyword)
        if not results:
            print("Книги не найдены.")
        else:
            for book in results:
                print(book)


    def display_books(self) -> None:
        """
        Отображение всех книг
        """
        self.library.display_books()


    def update_status(self) -> None:
        """
        Изменение статуса книги.
        """
        try:
            book_id = int(input("Введите ID книги для обновления статуса: "))
            status = input("Введите новый статус ('в наличии' или 'выдана'): ").strip()
            self.library.update_status(book_id, status)
        except ValueError:
            print("ID должен быть числом.")


    def exit_program(self) -> None:
        """
        Завершение работы программы
        """
        print("Выход из программы")
        self.running = False