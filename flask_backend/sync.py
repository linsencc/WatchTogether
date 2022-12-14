import functools
from app import socketio
from app import socketio_namespace


class User:
    def __init__(self, email: str, nickname: str):
        self.email = email
        self.nickname = nickname

        self._socketio = False
        self._url = None
        self._video_state = -1  # onload oncanplay onplaying onpause
        self._video_progress = -1

    @staticmethod
    def keys():
        return 'email', 'nickname', 'url', 'socketio', 'video_state', 'video_progress'

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url: str):
        self._url = url

    @property
    def socketio(self):
        return self._socketio

    @socketio.setter
    def socketio(self, value):
        self._socketio = value

    @property
    def video_state(self):
        return self._video_state

    @video_state.setter
    def video_state(self, state: int):
        self._video_state = state

    @property
    def video_progress(self):
        return self._video_progress

    @video_progress.setter
    def video_progress(self, progress: int):
        self._video_progress = progress


class Room:
    def __init__(self, room_number: str):
        self.room_number: str = room_number
        self.users: dict[str, User] = {}  # email -> user

    def get_users_info(self):
        # 获取对象的字典表示形式
        data = {k: dict(v) for k, v in self.users.items()}
        return data

    @staticmethod
    def user_info_change_notify(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            data = self.get_users_info()
            socketio.emit('', data, namespace=socketio_namespace)
            return res

        return wrapper

    @user_info_change_notify
    def add_user(self, user: User) -> bool:
        email = user.email

        if email not in self.users:
            self.users[email] = user
            return True

        return False

    @user_info_change_notify
    def delete_user(self, email: str) -> bool:
        if email in self.users:
            del self.users[email]
            return True

        return False

    def all_user_canplay(self) -> bool:
        for email, user in self.users.items():
            if user.video_state == 'xxx':
                return False

        return True

    def emit_play_order(self) -> bool:
        pass

    def emit_pause_order(self) -> bool:
        pass

    @user_info_change_notify
    def set_user_video_progress(self, email: str, video_progress: int) -> bool:
        if email in self.users:
            user = self.users[email]
            user.video_progress = video_progress
            return True

        return False

    @user_info_change_notify
    def set_user_video_state(self, email: str, video_state: int) -> bool:
        if email in self.users:
            user = self.users[email]
            user.video_state = video_state
            return True

        return False


class Manage:
    def __init__(self):
        self.rooms: dict[str, Room] = {}  # room number -> room
        self.user_to_room: dict[str, Room] = {}  # email -> room

    def get_room(self, room_number: str):
        if room_number in self.rooms:
            room = self.rooms[room_number]
            return room
        return None

    def create_room(self, room_number):
        if room_number not in self.rooms:
            room = Room(room_number)
            self.rooms[room_number] = room
            return room
        return None

    def delete_room(self, room_number: str) -> bool:
        if room_number in self.rooms:
            del self.rooms[room_number]
            return True
        return False

    def get_room_by_user(self, email: str):
        if email in self.user_to_room[email]:
            return self.user_to_room[email]
        return None

    def create_user_to_room(self, email: str, room: Room) -> bool:
        if email not in self.user_to_room:
            self.user_to_room[email] = room
            return True
        return False

    def delete_user_to_room(self, email: str) -> bool:
        if email in self.user_to_room:
            del self.user_to_room[email]
            return True
        return False
