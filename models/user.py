class User:
    """
    id - Уникальный идентификатор
    name - Имя пользователя
    email - Почта
    password - Пароль
    """

    def __init__(self, user_id: int, name: str, email: str, password: str):
        self.id = user_id
        self.name = name
        self.email = email
        self.password = password


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id_val: int):
        if not isinstance(id_val, int):
            raise TypeError("ID пользователя должен быть целым числом.")
        if id_val <= 0:
            raise ValueError("ID пользователя должен быть положительным числом.")
        self._id = id_val

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name_val: str):
        if not isinstance(name_val, str):
            raise TypeError("Имя пользователя должно быть строкой.")
        if len(name_val.strip()) < 1:
            raise ValueError('Имя пользователя не может быть пустым.')
        self._name = name_val.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email_val: str):
        if not isinstance(email_val, str):
            raise TypeError("Почта задается строкой.")
        if len(email_val.strip()) < 1:
            raise ValueError('Почта не может быть пустой.')
        self._name = email_val.strip()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password_val: str):
        if not isinstance(password_val, str):
            raise TypeError("Пароль задается строкой.")
        if len(password_val.strip()) < 1:
            raise ValueError('Пароль не может быть пустой.')
        if len(password_val) < 4:
            raise ValueError('Пароль должен состоять не менее, чем из 4 символов.')
        self._name = password_val.strip()
