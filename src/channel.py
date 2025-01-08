
import json
import os

from googleapiclient.discovery import build

class YouTubeMixin:
    """
        Класс для работы с YouTube API.

        Attributes:
            API_KEY (str): Ключ YouTube API, полученный из среды.
            YOUTUBE: Объект службы API YouTube.
    """
    API_KEY = os.getenv('API_KEY')
    YOUTUBE = build('youtube', 'v3', developerKey=API_KEY)

class Channel:
    """Класс для работы с каналом YouTube."""
    def __init__(self, channel_id: str) -> None:
        """
        Инициализирует экземпляр канала и получает данные о нем из API.

        :param self.__channel_id: Уникальный идентификатор канала YouTube

        Извлеченная информация сохраняется в следующих атрибутах объекта:
            self.title (str): Название канала.
            self.description (str): Описание канала.
            self.url (str): Ссылка на канал.
            self.subscriberCount (str): Количество подписчиков.
            self.video_count (str): Количество видео.
            self.viewCount (str): Количество просмотров.
        """
        self.__channel_id = channel_id
        channel = self.YOUTUBE.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.title = ''.join([x['snippet']['title'] for x in channel['items']])
        self.description = ''.join([x['snippet']['description'] for x in channel['items']])
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriberCount = ''.join([x['statistics']['subscriberCount'] for x in channel['items']])
        self.video_count = ''.join([x['statistics']['videoCount'] for x in channel['items']])
        self.viewCount = ''.join([x['statistics']['viewCount'] for x in channel['items']])

    def __repr__(self):
        """Возвращает строковое представление объекта для разработчиков."""
        return f"Channel(id={self.__channel_id}"

    def __str__(self) -> str:
        """Возвращает строковое представление объекта для пользователей."""
        return f"{self.title} ({self.url})"

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

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.YOUTUBE.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))
