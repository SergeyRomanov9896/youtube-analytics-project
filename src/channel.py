import json
import os

from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.title = ''.join([x['snippet']['title'] for x in channel['items']])
        self.description = ''.join([x['snippet']['description'] for x in channel['items']])
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriberCount = ''.join([x['statistics']['subscriberCount'] for x in channel['items']])
        self.video_count = ''.join([x['statistics']['videoCount'] for x in channel['items']])
        self.viewCount = ''.join([x['statistics']['viewCount'] for x in channel['items']])

    def __str__(self) -> str:
        return f"{self.title} ({self.url})"

    @property
    def channel_id(self) -> str:
        """Возвращает id канала."""
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, new_id: str) -> None:
        """Не дает изменять id канала."""
        if self.__channel_id == new_id:
            raise ValueError("AttributeError: property 'channel_id' of 'Channel' object has no setter")

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с API."""
        return cls.youtube

    def to_json(self, path: str) -> None:
        """Сохраняет данные о канале в json-файл."""
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
        return int(self.subscriberCount) + int(other.subscriberCount)

    def __sub__(self, other) -> int:
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __gt__(self, other) -> bool:
        return int(self.subscriberCount) > int(other.subscriberCount)

    def __ge__(self, other) -> bool:
        return int(self.subscriberCount) >= int(other.subscriberCount)

    def __lt__(self, other) -> bool:
        return int(self.subscriberCount) < int(other.subscriberCount)

    def __le__(self, other) -> bool:
        return int(self.subscriberCount) <= int(other.subscriberCount)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        def printj(dict_to_print: dict) -> None:
            """Выводит словарь в json-подобном удобном формате с отступами"""
            print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        printj(channel)
