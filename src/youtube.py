
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
