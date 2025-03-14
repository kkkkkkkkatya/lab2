from datetime import date, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Constants
BORROW_PERIOD = timedelta(days=14)
DEFAULT_COPIES = 1


class Book:
    def __init__(self, title, author, copies=DEFAULT_COPIES):
        self.title = title
        self.author = author
        self.copies = copies

    def is_available(self):
        return self.copies > 0

    def borrow(self):
        if self.is_available():
            self.copies -= 1

    def return_book(self):
        self.copies += 1


class User:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.is_available():
            book.borrow()
            self._add_borrow_record(book)
        else:
            logger.error(f"{self.name} не може взяти '{book.title}', бо її немає в наявності.")

    def _add_borrow_record(self, book):
        self.borrowed_books.append((book, date.today(), date.today() + BORROW_PERIOD))

    def return_book(self, book):
        for record in self.borrowed_books:
            if record[0] == book:
                book.return_book()
                self.borrowed_books.remove(record)
                return
        logger.error(f"{self.name} не має книги '{book.title}' в списку позик.")

    def list_borrowed_books(self):
        if not self.borrowed_books:
            print(f"{self.name} не взяв жодної книги.")
            return

        print(f"\n{self.name} взяв такі книги:")
        for record in self.borrowed_books:
            print(f"- {record[0].title} (повернути до {record[2]})")


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title, author, copies=DEFAULT_COPIES):
        self.books.append(Book(title, author, copies))

    def find_book(self, title):
        return next((book for book in self.books if book.title.lower() == title.lower()), None)

    def borrow_book(self, user, title):
        book = self.find_book(title)
        if book:
            user.borrow_book(book)
        else:
            logger.error(f"Книга '{title}' не знайдена у бібліотеці.")

    def return_book(self, user, title):
        book = self.find_book(title)
        if book:
            user.return_book(book)
        else:
            logger.error(f"Книга '{title}' не знайдена у бібліотеці.")


# Використання системи
library = Library()
library.add_book("Гаррі Поттер", "Дж. К. Ролінг", 3)
library.add_book("1984", "Джордж Орвелл", 2)
library.add_book("Преступление и наказание", "Ф. Достоевський", 1)

user1 = User("Анна")
user2 = User("Олег")

library.borrow_book(user1, "Гаррі Поттер")
library.borrow_book(user2, "1984")
library.borrow_book(user2, "Преступление і наказание")

user1.list_borrowed_books()
user2.list_borrowed_books()

library.return_book(user1, "Гаррі Поттер")
library.return_book(user2, "1984")

user1.list_borrowed_books()
user2.list_borrowed_books()
