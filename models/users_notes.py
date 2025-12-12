from .user import User
from .note import Note

class UserNote:
    def __init__(self, user: User, note: Note, un_id: int):
        self.user = user
        self.note = note
        self.id = un_id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id_val: int):
        if not isinstance(id_val, int):
            raise TypeError("ID должен быть целым числом.")
        if id_val <= 0:
            raise ValueError("ID должен быть положительным числом.")
        self.__id = id_val

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user_obj: User):
        if not isinstance(user_obj, User):
            raise TypeError("Пользователь должен быть объектом класса User.")
        self.__user = user_obj

    @property
    def note(self):
        return self.__note

    @note.setter
    def note(self, note_obj: Note):
        if not isinstance(note_obj, Note):
            raise TypeError("Заметка должна быть объектом класса Note.")
        self.__note = note_obj