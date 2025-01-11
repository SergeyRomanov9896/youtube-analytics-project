
import json

from src.youtube import YouTubeMixin

class Channel(YouTubeMixin):
    """Класс для работы с каналом YouTube."""
    def __init__(self, channel_id: str) -> None:
        """
        Инициализирует экземпляр канала и получает данные о нем из API.

        :param self.__channel_id (str): Уникальный идентификатор канала YouTube

        Извлеченная информация сохраняется в следующих атрибутах объекта:
            channel_response (dict): Ответ от API YouTube с информацией о канале.
            title (str): Название канала.
            description (str): Описание канала.
            url (str): Ссылка на канал.
            subscriberCount (str): Количество подписчиков.
            video_count (str): Количество видео.
            viewCount (str): Количество просмотров.
        """
        self.__channel_id = channel_id
        self.channel_response = self.YOUTUBE.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = ''.join([x['snippet']['title'] for x in self.channel_response['items']])
        self.description = ''.join([x['snippet']['description'] for x in self.channel_response['items']])
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriberCount = ''.join([x['statistics']['subscriberCount'] for x in self.channel_response['items']])
        self.video_count = ''.join([x['statistics']['videoCount'] for x in self.channel_response['items']])
        self.viewCount = ''.join([x['statistics']['viewCount'] for x in self.channel_response['items']])

    def __repr__(self):
        """
        Возвращает строковое представление объекта для разработчиков.

        :return: Уникальный идентификатор канала YouTube
        """
        return f"{self.__class__.__name__}{self.__channel_id}"

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта для пользователей.

        :return: Название канала и ссылка на канал
        """
        return f"{self.title} ({self.url})"

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel_response, indent=2, ensure_ascii=False))

    @property
    def channel_id(self) -> str:
        """Возвращает id канала."""
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, new_id: str) -> None:
        """
        Не дает изменять id канала.

        :param new_id: Новый уникальный идентификатор канала YouTube
        :raises ValueError: Если попытается изменить id канала, вызывается исключение ValueError.
        """
        if self.__channel_id == new_id:
            raise ValueError("AttributeError: property 'channel_id' of 'Channel' object has no setter")

    @classmethod
    def get_service(cls):
        """Возвращает объект службы API YouTube."""
        return cls.YOUTUBE

    def to_json(self, path: str) -> None:
        """
        Сохраняет данные о канале в json-файл.

        :param path: Путь к файлу, куда сохранять данные.
        """
        data = {"id": self.__channel_id,
                 "title": self.title,
                 "description": self.description,
                 "url": self.url,
                 "subscriberCount": self.subscriberCount,
                 "videoCount": self.video_count,
                 "viewCount": self.viewCount,
                 }

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def __add__(self, other) -> int:
        """Возвращает сумму подписчиков двух каналов."""
        return int(self.subscriberCount) + int(other.subscriberCount)

    def __sub__(self, other) -> int:
        """Возвращает разницу подписчиков двух каналов."""
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __gt__(self, other) -> bool:
        """Возвращает True, если подписчики первого канала больше второго, иначе False."""
        return int(self.subscriberCount) > int(other.subscriberCount)

    def __ge__(self, other) -> bool:
        """Возвращает True, если подписчики первого канала не меньше второго, иначе False."""
        return int(self.subscriberCount) >= int(other.subscriberCount)

    def __lt__(self, other) -> bool:
        """Возвращает True, если подписчики первого канала меньше второго, иначе False."""
        return int(self.subscriberCount) < int(other.subscriberCount)

    def __le__(self, other) -> bool:
        """Возвращает True, если подписчики первого канала не меньше второго, иначе False."""
        return int(self.subscriberCount) <= int(other.subscriberCount)
