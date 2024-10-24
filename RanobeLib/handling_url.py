import os
import re
from urllib.parse import urlparse

class UrlCreate:
    def __init__(self, url: str, msg_manager):
        self.project_url = url
        self.project_dir = None
        self.is_special = False
        self.msg_manager = msg_manager

    # Получение данных о проекте из введённой ссылки, создание папки для проекта
    def give_project(self) -> None:
        # Проверка валидности URL
        if not self.is_valid_url(self.project_url):
            self.msg_manager.show_message('invalid_url')
            return
            
        
        # Извлечение данных из ссылки
        result = self.parse_url(self.project_url)
        
        # Если парсинг не удался, выходим
        if result == (None, None, None, None):
            self.msg_manager.show_message('invalid_url')
            return

        # Извлечение данных из ссылки
        self.project_id, self.original_name_project, self.volume, self.chapter = self.parse_url(self.project_url)

        # Преобразование названия проекта
        self.name_project = self.format_project_name(self.original_name_project)

        # Создание директории
        self.create_dir()

    # Проверка валидности URL
    def is_valid_url(self, url: str) -> bool:
        parsed_url = urlparse(url)
        # Проверяем, что у ссылки есть схема и хост
        return bool(parsed_url.scheme and parsed_url.netloc)

    # Преобразование названия проекта (замена "-" на пробелы и преобразование к title-case)
    def format_project_name(self, name: str) -> str:
        return name.replace('-', ' ').title()

    # Парсинг URL-адреса для извлечения названия проекта, номера тома и главы
    def parse_url(self, url: str) -> tuple:
        url = self.clean_url(url)

        project_pattern = r"https://ranobelib.me/ru/book/(\d+)--([a-zA-Z0-9\-]+)"
        chapter_pattern = r"https://ranobelib.me/ru/(\d+)--([a-zA-Z0-9\-]+)/read/v(\d+)/c(\d+)"

        # Проверка URL проекта
        if project_match := re.search(project_pattern, url):
            project_id, name_project = project_match.group(1), project_match.group(2)
            return project_id, name_project, None, None
        
        # Проверка URL главы
        elif chapter_match := re.search(chapter_pattern, url):
            project_id, name_project, volume, chapter = chapter_match.groups()
            return project_id, name_project, int(volume), int(chapter)

       # Вместо raise ValueError, выводим сообщение и возвращаем None
        return None, None, None, None

    # Очистка URL от параметров
    def clean_url(self, url: str) -> str:
        url = self.check_special_symbol(url)
        return url.split('?')[0]

    # Создание директории для проекта
    def create_dir(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_dir = os.path.join(current_dir, self.name_project)

        if not self.safe_create_dir(self.project_dir):
            self.msg_manager.show_message('folder_already_creat')

    # Безопасное создание директории
    def safe_create_dir(self, path: str) -> bool:
        try:
            os.makedirs(path, exist_ok=True)
            self.msg_manager.show_message('folder_creat')
            return True
        except OSError as e:
        # Используем новое сообщение для отображения ошибки
            self.msg_manager.show_message('folder_creation_error', str(e))
            return False

    # Проверка и удаление спецсимвола
    def check_special_symbol(self, url: str) -> str:
        special_symbol = '$'
        if url.startswith(special_symbol + ' '):
            self.is_special = True
            url = url[2:]
            self.msg_manager.show_message('folder_already_creat')
        return url

    def check_chapter_and_volume(self, url_template):
        return re.search(r'/v(\d+)/c([\d.]+)', url_template)