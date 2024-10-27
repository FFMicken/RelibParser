from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NovelManager:
    def __init__(self, driver, document_manager, msg_manager):
        self.__driver = driver
        self.__document_manager = document_manager
        self.msg_manager = msg_manager
        self.html_code = None
        self.timeout = 50

    def click_element(self, by, value):
        element = WebDriverWait(self.__driver, self.timeout).until(EC.element_to_be_clickable((by, value)))
        self.__driver.execute_script("arguments[0].click();", element)

    def save_html(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(self.html_code)

    def open_project_or_chapters(self, project):
        if project.volume is None and project.chapter is None:
            self.open_first_chapter(project)
        else:
            url_template = f"https://ranobelib.me/ru/{project.project_id}--{project.original_name_project}/read/v{project.volume}/c{project.chapter}"
            self.save_chapters(project, url_template)

    def open_first_chapter(self, project):
        url_template = f"https://ranobelib.me/ru/book/{project.project_id}--{project.original_name_project}?section=info"
        self.__driver.get(url_template)

        try:
            if project.is_special:
                self.html_code = self.__driver.page_source
                self.save_html("project_page.html")

            project_link = f"/ru/{project.project_id}--{project.original_name_project}/read/v01/c01"
            self.click_element(By.XPATH, f"//a[@href='{project_link}' and contains(@class, 'btn') and contains(@class, 'is-filled') and contains(@class, 'variant-primary')]")

            WebDriverWait(self.__driver, self.timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
            
            url_template = self.__driver.current_url

            project.project_id, project.original_name_project, project.volume, project.chapter = project.parse_url(url_template)

            self.open_project_or_chapters(project)
            
        except Exception as e:
            self.log_error('project_opening_error', e)

    def save_chapters(self, project, url_template):
        while True:
            try:
                WebDriverWait(self.__driver, self.timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

                if "404" in self.__driver.current_url:
                    self.msg_manager.show_message('error_404', url_template)
                    break

                self.update_project_info(project)

                if self.is_chapter_saved(project.volume, project.chapter):
                    if not self.navigate_to_next_page("//span[text()='Вперёд']", project):
                        break
                    continue

                self.msg_manager.show_message('current_volume_and_chapter', project.volume, project.chapter)
                
                self.__document_manager.save_chapter(project.chapter, self.__driver, project)

                if not self.navigate_to_next_page("//span[text()='Вперёд']", project):
                    break

            except Exception as e:
                self.log_error('there_was_an_error', e)
                break

        self.__document_manager.save_document()

    def is_chapter_saved(self, volume, chapter):
        return volume in self.__document_manager.saved_chapters and chapter in self.__document_manager.saved_chapters[volume]

    def navigate_to_next_page(self, xpath, project):
        buttons = self.__driver.find_elements(By.XPATH, xpath)
        if buttons:
            self.__driver.execute_script("arguments[0].click();", buttons[0])
            project.is_special = False
            return True
        return False
    
    def update_project_info(self, project):
        url_template = self.__driver.current_url
        match = project.check_chapter_and_volume(url_template)
        if match:
            project.volume = match.group(1)
            project.chapter = match.group(2)

    def log_error(self, error_type, exception):
        self.msg_manager.show_message(error_type, exception)