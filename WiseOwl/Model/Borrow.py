# Model/Borrow.py
class Borrow:
    def __init__(self, record_id=None, member_id="", book_id="", book_title="",
                 borrow_date="", due_date="", return_date="", status="Borrowed"):
        self.record_id = record_id
        self.member_id = member_id
        self.book_id = book_id
        self.book_title = book_title
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = return_date
        self.status = status

    def is_overdue(self):
        """Check if book is overdue (simplified version)"""
        if self.status == "Returned" or not self.due_date:
            return False
        # Simplified check - in real app, compare with current date
        return "Overdue" in self.due_date or "Due:" in self.due_date

    def get_history_data(self):
        """Get data for history display"""
        return {
            "title": self.book_title,
            "borrow_date": self.borrow_date,
            "return_date": self.return_date,
            "status": self.status
        }