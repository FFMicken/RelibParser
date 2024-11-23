import os

from save_to_docx import DocxManager
from save_to_pdf import save_document_to_pdf
from save_to_fb2 import save_document_to_fb2
from save_to_epub import save_document_to_epub

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DocumentManager:
    def __init__(self, current_dir, project_dir, name_project, msg_manager, formats):
        self.current_dir = current_dir
        self.project_dir = project_dir
        self.name_project = name_project
        self.msg_manager = msg_manager
        self.formats = formats
        self.timeout = 50
        self.header_p = None
        self.chapter_title = None
        self.docx_manager = DocxManager(self.project_dir, self.name_project, self.msg_manager)
        
        self.title_ru = None
        self.title_en = None
        self.type = None
        self.format = None
        self.release_year = None
        self.chapters = None
        self.translator = None
        self.translator_team = None
        self.rating = None
        self.description = None
        self.genres = []

    def save_html(self, soup, volume, chapter, project_dir, caller):
        if caller == "save_info_and_nomber":
            html_file_path = os.path.join(project_dir, "title_info.html")
        else:
            html_file_path = os.path.join(project_dir, f"volume_{volume}_chapter_{chapter}.html")
        
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

        self.msg_manager.show_message('html_chapter_saved', chapter if caller != "save_info_and_nomber" else "title_info")

    def save_info_and_nomber(self, driver, project):
        WebDriverWait(driver, self.timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        main_page_data = {
            'Название (русское)': (soup.find('h1', class_='n7_n9').text.strip() 
                                if soup.find('h1', class_='n7_n9') else None),
            'Название (английское)': (soup.find('h2', class_='n7_oa').text.strip() 
                                    if soup.find('h2', class_='n7_oa') else None),
            'Тип': (soup.find('a', class_='v5_a5', href=lambda x: 'type%5B%5D' in x)
                    .find('span').text.strip() if soup.find('a', class_='v5_a5', href=lambda x: 'type%5B%5D' in x) else None),
            'Формат': (soup.find('div', text='Формат').find_next('a').text.strip() 
                    if soup.find('div', text='Формат') and soup.find('div', text='Формат').find_next('a') else None),
            'Год выпуска': (soup.find('a', class_='v5_a5', href=lambda x: 'year_min' in x)
                            .find('span').text.strip() if soup.find('a', class_='v5_a5', href=lambda x: 'year_min' in x) else None),
            'Количество глав': (soup.find('div', class_='tabs-item _variant-default')
                                .find('small').text.strip() if soup.find('div', class_='tabs-item _variant-default') else None),
            'Переводчик': (soup.find('div', class_='team-item__name').text.strip() 
                        if soup.find('div', class_='team-item__name') else None),
            'Оценка': (soup.find('span', class_='rating-info__value').text.strip() 
                    if soup.find('span', class_='rating-info__value') else None),
            'Описание': (soup.find('div', class_='vu_af').text.strip() 
                        if soup.find('div', class_='vu_af') else None),
            'Жанры': ([genre.text.strip() for genre in soup.find_all('a', {'data-type': 'genre'})] 
                    if soup.find_all('a', {'data-type': 'genre'}) else None)
        }

        if project.is_special:
            self.save_html(soup, volume=None, chapter=None, project_dir=self.project_dir, caller="save_info_and_nomber")

        try:
            self.docx_manager.save_main_page_info(main_page_data)

        except Exception as e:
            self.msg_manager.show_message('error_saving_main_page_info', str(e))

    def save_chapter(self, chapter, driver, project):
        WebDriverWait(driver, self.timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        if project.is_special:
            self.save_html(soup, volume=project.volume, chapter=chapter, project_dir=self.project_dir, caller="save_chapter")

        header_h1 = soup.find_all('h1')
        self.header_p = soup.find_all('p')
        h1_texts = [h1.get_text(strip=True) for h1 in header_h1]
        self.chapter_title = h1_texts[0] if h1_texts else f"Глава {chapter}"

        for format in self.formats:
            try:
                if format == '1':
                    self.docx_manager.save_chapter(self.chapter_title, self.header_p)
                elif format == '2':
                    save_document_to_pdf(self)
                elif format == '3':
                    save_document_to_fb2(self)
                elif format == '4':
                    save_document_to_epub(self)
            except Exception as e:
                self.msg_manager.show_message('error_saving_in_format', format, str(e))

        self.msg_manager.show_message('current_volume_and_chapter', project.volume, project.chapter)
        
        return True

    def save_document(self):
        self.msg_manager.show_message('all_chapters_are_saved_to', self.project_dir)

    def finalize(self):
        self.docx_manager.finalize()
