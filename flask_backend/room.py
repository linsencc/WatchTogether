from .user import User


class Room:
    def __init__(self, room_id: str, web_url: str):
        self.room_id = room_id
        self.web_url = web_url
        self.users = []

    def add_user(self, user: User):
        self.users.append(user)

    def delete_user(self, user: User):
        self.users.remove(user)
        