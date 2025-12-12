from typing import Union

class Note:
    """
    Класс для представления заметки.
    
    Атрибуты:
    id (str): Индекс заметки.
    title (str): Заголовок заметки.
    discription (str): Текст заметки.
    data_create (str): Дата создания.
    data_update (str): Дата обновления.
    tags (str): Теги, связанные с заметкой.
    """

    def __init__(self, id: str, title: str, discription: str, data_create: str, data_update: str, tags: str):
        self.__id: str = id
        self.__title: str = title
        self.__discription: str = discription
        self.__data_create: str = data_create 
        self.__data_update: str = data_update
        self.__tags: str = tags


    @property
    def id(self) -> str:
        """Получает ID заметки."""
        return self.__id

    @id.setter
    def id(self, id_val: str):
        """Устанавливает ID заметки с проверкой."""
        if not isinstance(id_val, str):
            raise TypeError("ID заметки должен быть строкой.")
        if len(id_val) >= 1:
            self.__id = id_val
        else:
            raise ValueError('ID заметка не может быть пустой.')

    @property
    def title(self) -> str:
        """Получает заголовок заметки."""
        return self.__title

    @title.setter
    def title(self, title_val: str):
        """Устанавливает заголовок заметки с проверкой."""
        if not isinstance(title_val, str):
            raise TypeError("Заголовок должен быть строкой.")
        self.__title = title_val

    @property
    def discription(self) -> str:
        """Получает текст/описание заметки."""
        return self.__discription

    @discription.setter
    def discription(self, discription_val: str):
        """Устанавливает текст/описание заметки с проверкой."""
        if not isinstance(discription_val, str):
            raise TypeError("Описание должно быть строкой.")
        self.__discription = discription_val

    @property
    def data_create(self) -> str:
        """Получает дату создания заметки."""
        return self.__data_create

    @property
    def data_update(self) -> str:
        """Получает дату обновления заметки."""
        return self.__data_update

    @data_update.setter
    def data_update(self, date_update_val: str):
        """Устанавливает дату обновления заметки с проверкой."""
        if not isinstance(date_update_val, str):
             raise TypeError("Дата обновления должна быть строкой.")
        self.__data_update = date_update_val

    @property
    def tags(self) -> str:
        """Получает теги заметки."""
        return self.__tags

    @tags.setter
    def tags(self, tags_val: str):
        """Устанавливает теги заметки с проверкой."""
        if not isinstance(tags_val, str):
            raise TypeError("Теги должны быть строкой.")
        self.__tags = tags_val

