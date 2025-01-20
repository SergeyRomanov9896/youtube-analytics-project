
from src.youtube import YouTubeMixin

class Video(YouTubeMixin):
    """Класс для работы с видео YouTube."""
    def __init__(self, video_id: str) -> None:
        """
        Извлекает информацию о видео с помощью YouTube Data API v3

        :param video_id: id видео

        Извлеченная информация сохраняется в следующих атрибутах объекта:
            video_response (dict): Ответ от API YouTube с информацией о видео.
            title (str): Заголовок видео
            url (str): Ссылка на видео
            view_count (str): Количество просмотров видео
            like_count (str): Количество лайков видео
        """
        self.video_id = video_id
        try:
            self.video_response = self.YOUTUBE.videos().list(part='snippet,statistics', id=self.video_id).execute()
            video_data = self.video_response['items'][0]
            self.title = video_data['snippet']['title']
            self.like_count = video_data['statistics']['likeCount']
            self.url = f'https://www.youtube.com/watch?v={self.video_id}'
            self.view_count = video_data['statistics']['viewCount']
        except IndexError:
            self.video_id = video_id
            self.title = None
            self.like_count = None
            self.url = None
            self.view_count = None
    def __repr__(self):
        """
        Возвращает строковое представление объекта для разработчиков.

        :return: Уникальный идентификатор видео YouTube
        """
        return f"{self.__class__.__name__}{self.video_id}"

    def __str__(self):
        """
        Возвращает строковое представление объекта для пользователей.

        :return: Заголовок видео
        """
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
        """
        Возвращает строковое представление объекта для разработчиков.

        :return: Уникальный идентификатор видео YouTube и идентификатор плейлиста
        """
        return f"{self.__class__.__name__}{self.video_id}, title={self.playlist_id})"

    def __str__(self):
        """
        Возвращает строковое представление объекта для разработчиков.

        :return: Заголовок видео
        """
        return f"{self.title}"
