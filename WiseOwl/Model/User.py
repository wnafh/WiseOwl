# Model/User.py
class User:
    def __init__(self, user_name, member_id, role):
        self.user_name = user_name
        self.member_id = member_id
        self.role = role

    def is_admin(self):
        return self.role == "Library Admin"

    def is_user(self):
        return self.role == "Library User"

    def get_info(self):
        return {
            "user_name": self.user_name,
            "member_id": self.member_id,
            "role": self.role
        }