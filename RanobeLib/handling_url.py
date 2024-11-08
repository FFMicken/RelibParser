import os
import re
from urllib.parse import urlparse

class UrlCreate:
    def __init__(self, url, msg_manager):
        self.project_url = url
        self.project_dir = None
        self.is_special = False
        self.msg_manager = msg_manager

    def give_project(self):
        self.clean_url(self.project_url)
        
        if not self.is_valid_url(self.project_url):
            self.msg_manager.show_message('invalid_url')
            return    
        
        self.project_id, self.original_name_project, self.volume, self.chapter = self.parse_url(self.project_url)
        
        if self.project_id and self.original_name_project and self.volume and self.chapter == None:
            self.msg_manager.show_message('invalid_url')
            return

        self.name_project = self.format_project_name(self.original_name_project)

        self.create_dir()

    def is_valid_url(self, url):
        parsed_url = urlparse(url)
        return bool(parsed_url.scheme and parsed_url.netloc)

    def format_project_name(self, name):
        return name.replace('-', ' ').title()

    def parse_url(self, url):

        project_pattern = r"https://ranobelib.me/ru/book/(\d+)--([a-zA-Z0-9\-]+)"
        chapter_pattern = r"https://ranobelib.me/ru/(\d+)--([a-zA-Z0-9\-]+)/read/v(\d+)/c(\d+)"

        if project_match := re.search(project_pattern, url):
            project_id, name_project = project_match.group(1), project_match.group(2)
            return project_id, name_project, None, None
        
        elif chapter_match := re.search(chapter_pattern, url):
            project_id, name_project, volume, chapter = chapter_match.groups()
            return project_id, name_project, int(volume), int(chapter)

        return None, None, None, None

    def clean_url(self, url):
        self.project_url = self.check_special_symbol(url)
        self.project_url.split('?')[0]

    def create_dir(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_dir = os.path.join(current_dir, self.name_project)

        if not self.safe_create_dir(self.project_dir):
            self.msg_manager.show_message('folder_already_creat')

    def safe_create_dir(self, path):
        try:
            os.makedirs(path, exist_ok=True)
            self.msg_manager.show_message('folder_creat')
            return True
        except OSError as e:

            self.msg_manager.show_message('folder_creation_error', str(e))
            return False

    def check_special_symbol(self, url):
        special_symbol = '$'
        if url.startswith(special_symbol + ' '):
            self.is_special = True
            url = url[2:]
            self.msg_manager.show_message('special symbol found')
        return url

    def check_chapter_and_volume(self, url_template):
        return re.search(r'/v(\d+)/c([\d.]+)', url_template)