import unittest

from before import Library, User


class TestLibrarySystem(unittest.TestCase):

    def setUp(self):
        """Set up a library with some books and users for testing."""
        self.library = Library()
        self.library.add_book("Гаррі Поттер", "Дж. К. Ролінг", 3)
        self.library.add_book("1984", "Джордж Орвелл", 2)
        self.library.add_book("Преступление и наказание", "Ф. Достоевський", 1)

        self.user1 = User("Анна")
        self.user2 = User("Олег")

    def test_book_availability(self):
        """Test if a book is available."""
        book = self.library.find_book("Гаррі Поттер")
        self.assertTrue(book.is_available())

    def test_borrow_book_success(self):
        """Test borrowing a book successfully."""
        self.library.borrow_book(self.user1, "Гаррі Поттер")
        self.assertEqual(len(self.user1.borrowed_books), 1)

    def test_borrow_book_unavailable(self):
        """Test borrowing a book that is not available after exhausting copies."""
        # Borrow the available copies first
        self.library.borrow_book(self.user1, "1984")  # Borrow 1
        self.library.borrow_book(self.user1, "1984")  # Borrow 2
        # At this point, all copies of "1984" are borrowed, so the next borrow should fail
        self.library.borrow_book(self.user1, "1984")  # Attempt to borrow again

        # Assert that the number of borrowed books is still 2
        self.assertEqual(len(self.user1.borrowed_books), 2)  # Should still be 2

    def test_return_book_success(self):
        """Test returning a book successfully."""
        self.library.borrow_book(self.user1, "Гаррі Поттер")
        self.library.return_book(self.user1, "Гаррі Поттер")
        self.assertEqual(len(self.user1.borrowed_books), 0)

    def test_return_book_not_borrowed(self):
        """Test returning a book that was not borrowed."""
        self.library.return_book(self.user1, "Гаррі Поттер")
        self.assertEqual(len(self.user1.borrowed_books), 0)

    def test_borrow_book_not_found(self):
        """Test borrowing a book that does not exist in the library."""
        with self.assertLogs(level='ERROR'):
            self.library.borrow_book(self.user1, "Несуществующая книга")

    def test_return_book_not_found(self):
        """Test returning a book that does not exist in the library."""
        with self.assertLogs(level='ERROR'):
            self.library.return_book(self.user1, "Несуществующая книга")

    def test_list_borrowed_books(self):
        """Test listing borrowed books."""
        self.library.borrow_book(self.user1, "Гаррі Поттер")
        self.library.borrow_book(self.user1, "1984")
        self.user1.list_borrowed_books()
        self.assertEqual(len(self.user1.borrowed_books), 2)

    def test_borrow_multiple_books(self):
        """Test borrowing multiple books."""
        self.library.borrow_book(self.user1, "Гаррі Поттер")
        self.library.borrow_book(self.user1, "1984")
        self.library.borrow_book(self.user2, "Преступление и наказание")
        self.assertEqual(len(self.user1.borrowed_books), 2)
        self.assertEqual(len(self.user2.borrowed_books), 1)

    def test_book_copy_management(self):
        """Test book copy management after borrowing and returning."""
        book = self.library.find_book("Гаррі Поттер")
        self.assertEqual(book.copies, 3)
        self.library.borrow_book(self.user1, "Гаррі Поттер")
        self.assertEqual(book.copies, 2)
        self.library.return_book(self.user1, "Гаррі Поттер")
        self.assertEqual(book.copies, 3)

if __name__ == '__main__':
    unittest.main()
