class Note:
    def __init__(self, id: str, title: str, discription: str, data_create: str, data_update: str, tags: str):
        self.id = id
        self.title = title
        self.discription = discription
        self.data_create = data_create 
        self.data_update = data_update
        self.tags = tags

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, id_val: str):
        if not isinstance(id_val, str):
            raise TypeError("ID заметки должен быть строкой.")
        if len(id_val) >= 1:
            self.__id = id_val
        else:
            raise ValueError('ID заметки не может быть пустым.')

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title_val: str):
        if not isinstance(title_val, str):
            raise TypeError("Заголовок должен быть строкой.")
        self.__title = title_val

    @property
    def discription(self) -> str:
        return self.__discription

    @discription.setter
    def discription(self, discription_val: str):
        if not isinstance(discription_val, str):
            raise TypeError("Описание должно быть строкой.")
        self.__discription = discription_val

    @property
    def data_create(self) -> str:
        return self.__data_create

    @data_create.setter
    def data_create(self, data_create_val: str):
        if not isinstance(data_create_val, str):
            raise TypeError("Дата создания должна быть строкой.")
        self.__data_create = data_create_val

    @property
    def data_update(self) -> str:
        return self.__data_update

    @data_update.setter
    def data_update(self, data_update_val: str):
        if not isinstance(data_update_val, str):
            raise TypeError("Дата обновления должна быть строкой.")
        self.__data_update = data_update_val

    @property
    def tags(self) -> str:
        return self.__tags

    @tags.setter
    def tags(self, tags_val: str):
        if not isinstance(tags_val, str):
            raise TypeError("Теги должны быть строкой.")
        self.__tags = tags_val