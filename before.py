from datetime import date, timedelta

class Book:
    def __init__(self, title, author, copies):
        self.title = title
        self.author = author
        self.copies = copies

    def is_available(self):
        return self.copies > 0

    def borrow(self):
        if self.is_available():
            self.copies -= 1
        else:
            print(f"Книга '{self.title}' недоступна.")

    def return_book(self):
        self.copies += 1


class User:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.is_available():
            book.borrow()
            self.borrowed_books.append((book, date.today(), date.today() + timedelta(days=14)))
        else:
            print(f"{self.name} не може взяти '{book.title}', бо її немає в наявності.")

    def return_book(self, book):
        for record in self.borrowed_books:
            if record[0] == book:
                book.return_book()
                self.borrowed_books.remove(record)
                return
        print(f"{self.name} не має книги '{book.title}' в списку позик.")

    def list_borrowed_books(self):
        print(f"\n{self.name} взяв такі книги:")
        for record in self.borrowed_books:
            print(f"- {record[0].title} (повернути до {record[2]})")


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title, author, copies=1):
        self.books.append(Book(title, author, copies))

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def borrow_book(self, user, title):
        book = self.find_book(title)
        if book:
            user.borrow_book(book)
        else:
            print(f"Книга '{title}' не знайдена у бібліотеці.")

    def return_book(self, user, title):
        book = self.find_book(title)
        if book:
            user.return_book(book)
        else:
            print(f"Книга '{title}' не знайдена у бібліотеці.")


# Використання системи
library = Library()
library.add_book("Гаррі Поттер", "Дж. К. Ролінг", 3)
library.add_book("1984", "Джордж Орвелл", 2)
library.add_book("Преступление и наказание", "Ф. Достоевский", 1)

user1 = User("Анна")
user2 = User("Олег")

library.borrow_book(user1, "Гаррі Поттер")
library.borrow_book(user2, "1984")
library.borrow_book(user2, "Преступление и наказание")

user1.list_borrowed_books()
user2.list_borrowed_books()

library.return_book(user1, "Гаррі Поттер")
library.return_book(user2, "1984")

user1.list_borrowed_books()
user2.list_borrowed_books()

