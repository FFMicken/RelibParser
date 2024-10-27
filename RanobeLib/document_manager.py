import os

from save_to_docx import save_document_to_docx
from save_to_pdf import save_document_to_PDF
from save_to_fb2 import save_document_to_FB2
from save_to_epub import save_document_to_EPUB

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DocumentManager:
    def __init__(self, project_dir, name_project, msg_manager, formats):
        self.project_dir = project_dir
        self.name_project = name_project
        self.msg_manager = msg_manager
        self.saved_chapters = {}
        self.formats = formats
        self.chapters_buffer = [] 
    
    def get_saved_chapters(self):
        return self.saved_chapters

    def save_html(self, page_source, volume, chapter, project_dir):
        html_file_path = os.path.join(project_dir, f"volume_{volume}_chapter_{chapter}.html")
        
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write(page_source)

        self.msg_manager.show_message('html_chapter_saved', chapter)

    def save_chapter(self, chapter, driver, project):

        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.TAG_NAME, 'p')))

        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        if project.is_special:
            self.save_html(page_source, project.volume, project.chapter, project.project_dir)

        header_h1 = soup.find_all('h1')
        header_p = soup.find_all('p')

        h1_texts = [h1.get_text(strip=True) for h1 in header_h1]
        chapter_title = h1_texts[0] if h1_texts else f"Глава {chapter}"

        self.chapters_buffer.append((chapter_title, header_p))

        if project.volume not in self.saved_chapters:
            self.saved_chapters[project.volume] = []
        if chapter not in self.saved_chapters[project.volume]:
            self.saved_chapters[project.volume].append(chapter)

    def save_document(self):
        for format in self.formats:
            try:
                if format == '1':
                    save_document_to_docx(self)
                elif format == '2':
                    save_document_to_PDF(self)
                elif format == '3':
                    save_document_to_FB2(self)
                elif format == '4':
                    save_document_to_EPUB(self)
            except Exception as e:
                self.msg_manager.show_message(f'Ошибка при сохранении в формате {format}: {str(e)}')