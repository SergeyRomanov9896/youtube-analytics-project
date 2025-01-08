
import os
import datetime

import isodate
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

class PlayList(YouTubeMixin):
    """Класс для работы с каналом YouTube."""
    def __init__(self, playlist_id: str) -> None:
        """
        Инициализация объекта PlayList.

        :param playlist_id: - идентификатор плейлиста.

        Извлеченная информация сохраняется в следующих атрибутах объекта:
            playlist_id: Идентификатор плейлиста.
            playlist_response: Ответ от API YouTube с информацией о плейлисте.
            videos_id: Список идентификаторов видео в плейлисте.
            title: Название плейлиста.
            url: URL-адрес плейлиста.
        """
        self.playlist_id = playlist_id
        self.playlist_response = self.YOUTUBE.playlistItems().list(part='snippet,contentDetails',
                                              playlistId=self.playlist_id).execute()
        self.videos_id = [play_list["contentDetails"]["videoId"] for play_list in self.playlist_response['items']]
        self.title = ''.join([title['snippet']['title'] for title in self.playlist_response['items']]).split('.')[0]
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def __repr__(self):
        """Возвращает строковое представление объекта для разработчиков."""
        return f'{self.__class__.__name__}{self.playlist_id}'

    @property
    def total_duration(self):
        """Возвращает общее продолжительность видео в плейлисте."""
        total_duration = datetime.timedelta()
        video_response = self.YOUTUBE.videos().list(part='contentDetails',
                                              id=self.videos_id).execute()

        for video in video_response['items']:
            iso8601_format = video["contentDetails"]["duration"]
            durations = isodate.parse_duration(iso8601_format)
            total_duration += datetime.timedelta(seconds=durations.total_seconds())
        return total_duration

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео в плейлисте."""
        number_likes = []
        id = []

        for video in self.videos_id:
            video_response = self.YOUTUBE.videos().list(part='statistics',
                                                        id=video).execute()

            for items in video_response['items']:
                likes = items['statistics']['likeCount']
                number_likes.append(likes)
                id.append(items['id'])

        for rating in range(len(number_likes)):
            if number_likes[rating] == max(number_likes):
                return f'https://youtu.be/{id[rating]}'
