
import os
from googleapiclient.discovery import build

class Video:
    """Класс для работы с видео."""
    API_KEY = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    def __init__(self, video_id):
        """
        Инициализирует объект видео.
        :param video_id: str - id видео
        :param title: str - заголовок видео
        :param url: str - ссылка на видео
        :param view_count: int - количество просмотров видео
        :param like_count: int - количество лайков видео
        """
        self.video_id = video_id
        video_response = self.youtube.videos().list(part='snippet,statistics', id=self.video_id).execute()

        self.title = ''.join([title['snippet']['title'] for title in video_response['items']])
        self.url = f'https://www.youtube.com/watch?v={self.video_id}'
        self.view_count = ''.join([viewCount['statistics']['viewCount'] for viewCount in video_response['items']])
        self.like_count = ''.join([likeCount['statistics']['likeCount'] for likeCount in video_response['items']])

    def __str__(self):
        return f"{self.title}"

class PLVideo(Video):
    """Класс для работы с видео из плейлиста."""
    def __init__(self, video_id, playlist_id):
        """
        :param video_id: str - id видео
        :param playlist_id: str - id плейлиста
        """
        super().__init__(video_id)
        self.video_id = video_id
        self.playlist_id = playlist_id

    def __str__(self):
        return f"{self.title}"



