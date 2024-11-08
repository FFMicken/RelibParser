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
        self.formats = formats
        self.chapters_buffer = []

    def save_html(self, soup, volume, chapter, project_dir, caller):
        
        
        if caller == "save_info_and_nomber":
            html_file_path = os.path.join(project_dir, "title_info.html")
        else:
            html_file_path = os.path.join(project_dir, f"volume_{volume}_chapter_{chapter}.html")
        
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

        self.msg_manager.show_message('html_chapter_saved', chapter if caller != "save_info_and_nomber" else "title_info")

    def save_info_and_nomber(self, driver, project):
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        if project.is_special:
            self.save_html(soup, volume=None, chapter=None, project_dir=self.project_dir, caller="save_info_and_nomber")

    def save_chapter(self, chapter, driver, project):
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.TAG_NAME, 'p')))

        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        if project.is_special:
            self.save_html(soup, volume=project.volume, chapter=chapter, project_dir=self.project_dir, caller="save_chapter")

        header_h1 = soup.find_all('h1')
        header_p = soup.find_all('p')

        h1_texts = [h1.get_text(strip=True) for h1 in header_h1]
        chapter_title = h1_texts[0] if h1_texts else f"Глава {chapter}"

        self.chapters_buffer.append((chapter_title, header_p))

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
                self.msg_manager.show_message('error_saving_in_format', {format}, {str(e)})
