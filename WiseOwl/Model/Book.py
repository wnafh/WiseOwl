# Model/Book.py
class Book:
    def __init__(self, book_id=None, title="", author="", status="Available",
                 due_date="", isbn="", genre="", description=""):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.status = status
        self.due_date = due_date
        self.isbn = isbn
        self.genre = genre
        self.description = description

    def is_available(self):
        return self.status == "Available"

    def is_borrowed(self):
        return self.status == "Borrowed"

    def get_card_data(self):
        """Get data for UI card display"""
        return {
            "title": self.title,
            "author": f"by {self.author}",
            "due_date": self.due_date,
            "status": self.status
        }