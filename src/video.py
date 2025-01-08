
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

class Video(YouTubeMixin):
    """Класс для работы с видео YouTube."""
    def __init__(self, video_id: str) -> None:
        """
        Извлекает информацию о видео с помощью YouTube Data API v3

        :param video_id: id видео

        Извлеченная информация сохраняется в следующих атрибутах объекта:
            self.title (str): заголовок видео
            self.url (str): ссылка на видео
            self.view_count (str): количество просмотров видео
            self.like_count (str): количество лайков видео
        """
        self.video_id = video_id
        video_response = self.YOUTUBE.videos().list(part='snippet,statistics', id=self.video_id).execute()

        self.title = ''.join([title['snippet']['title'] for title in video_response['items']])
        self.url = f'https://www.youtube.com/watch?v={self.video_id}'
        self.view_count = ''.join([viewCount['statistics']['viewCount'] for viewCount in video_response['items']])
        self.like_count = ''.join([likeCount['statistics']['likeCount'] for likeCount in video_response['items']])

    def __repr__(self):
        """Возвращает строковое представление объекта для разработчиков."""
        return f"Video(id={self.video_id}"

    def __str__(self):
        """Возвращает строковое представление объекта для пользователей."""
        return f"{self.title}"

class PLVideo(Video):
    """Класс для работы с видео из плейлиста."""
    def __init__(self, video_id: str, playlist_id: str) -> None:
        """
        Инициализирует объект видео из плейлиста.

        :param video_id: - id видео
        :param playlist_id: - id плейлиста
        """
        super().__init__(video_id)
        self.video_id = video_id
        self.playlist_id = playlist_id

    def __repr__(self):
        """Возвращает строковое представление объекта для разработчиков."""
        return f"PLVideo(id={self.video_id}, title={self.playlist_id})"

    def __str__(self):
        """Возвращает строковое представление объекта для пользователей."""
        return f"{self.title}"



