import os
import zipfile
from bs4 import BeautifulSoup

def save_document_to_epub(self):
    try:
        epub_file_path = os.path.join(self.project_dir, f"{self.name_project}.epub")
        
        # Проверка на наличие файла и создание нового, если отсутствует
        if not os.path.exists(epub_file_path):
            with zipfile.ZipFile(epub_file_path, 'w') as epub:
                epub.writestr("mimetype", "application/epub+zip")
            temp_files = {}
        else:
            with zipfile.ZipFile(epub_file_path, 'r') as epub:
                temp_files = {name: epub.read(name) for name in epub.namelist()}

        # Подготовка заголовка и основного текста
        title_paragraph = f"<h1>{self.chapter_title}</h1>"
        main_text = '\n'.join([p.get_text(strip=True) for p in self.header_p if p.get_text(strip=True)])
        content_html = f"{title_paragraph}\n<p>{main_text}</p>"

        # Поиск основного контента для обновления или добавления
        content_file = "OEBPS/Text/chapter.xhtml"
        if content_file in temp_files:
            soup = BeautifulSoup(temp_files[content_file], 'html.parser')
            soup.body.append(BeautifulSoup(content_html, 'html.parser'))
            temp_files[content_file] = str(soup).encode('utf-8')
        else:
            soup = BeautifulSoup(f"<html><body>{content_html}</body></html>", 'html.parser')
            temp_files[content_file] = str(soup).encode('utf-8')

        # Запись в новый epub файл
        with zipfile.ZipFile(epub_file_path, 'w') as epub:
            for name, content in temp_files.items():
                epub.writestr(name, content)

        return epub_file_path

    except Exception as e:
        self.msg_manager.show_message('there_was_an_error', e)
