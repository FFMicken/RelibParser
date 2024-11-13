from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

class NovelManager:
    def __init__(self, driver, document_manager, msg_manager):
        self.__driver = driver
        self.__document_manager = document_manager
        self.msg_manager = msg_manager
        self.html_code = None
        self.timeout = 50
        self.saved_chapters = {}
        self.url_template = None

    def open_project_or_chapters(self, project):
        if project.volume is None and project.chapter is None:
            self.saveBookInfo(project)
            self.open_first_chapter(project)
        else:
            self.continue_save(project)
            self.save_chapters(project)

    def open_first_chapter(self, project):
        try:
            if project.is_special:
                self.html_code = self.__driver.page_source

            self.click_element(By.XPATH, "//span[@data-bookmark='false']")

            WebDriverWait(self.__driver, self.timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))

            self.url_template = self.__driver.current_url

            self.save_start_chapter(project)

            self.save_chapters(project)
            
        except Exception as e:
            self.log_error('project_opening_error', e)

    def saveBookInfo(self, project):
        self.url_template = f"https://ranobelib.me/ru/book/{project.project_id}--{project.original_name_project}?section=info"
        
        self.__driver.get(self.url_template)

        try:
            self.__document_manager.save_info_and_nomber(self.__driver, project)
            
        except Exception as e:
            self.log_error('project_opening_error', e)

    def save_start_chapter(self, project):

        project.project_id, project.original_name_project, project.volume, project.chapter = project.parse_url(self.url_template)

        self.__document_manager.save_chapter(project.chapter, self.__driver, project)

        self.add_chapter_in_dict(project)

    def continue_save(self, project):
        self.url_template = project.project_url

        self.__driver.get(self.url_template)

        self.save_start_chapter(project)

    def add_chapter_in_dict(self, project):
        if project.volume not in self.saved_chapters:
                self.saved_chapters[project.volume] = []
        if project.chapter not in self.saved_chapters[project.volume]:
                self.saved_chapters[project.volume].append(project.chapter)

    def click_element(self, by, value):
        element = WebDriverWait(self.__driver, self.timeout).until(EC.element_to_be_clickable((by, value)))
        self.__driver.execute_script("arguments[0].click();", element)

    def navigate_to_next_page(self, xpath, project):
        buttons = self.__driver.find_elements(By.XPATH, xpath)
        if buttons:
            self.__driver.execute_script("arguments[0].click();", buttons[0])
            project.is_special = False
            return True
        return False
    
    def update_project_info(self, project):
        self.url_template = self.__driver.current_url
        match = project.check_chapter_and_volume(self.url_template)
        if match:
            project.volume = match.group(1)
            project.chapter = match.group(2)

    def save_chapters(self, project):
        next_button_xpath = "//span[text()='Вперёд']"

        WebDriverWait(self.__driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, next_button_xpath)))
    
        while True:
            try:
                start_time = time.time()

                if self.navigate_to_next_page(next_button_xpath, project):
                    WebDriverWait(self.__driver, self.timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
                    WebDriverWait(self.__driver, self.timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'p')))

                    if self.__driver.current_url == "https://ranobelib.me/404":
                        self.msg_manager.show_message('error_404', self.url_template)
                        break

                    self.update_project_info(project)

                    if project.chapter in self.saved_chapters.get(project.volume, []):
                        self.update_project_info(project)
                        continue
                    
                    start_time_1 = time.time()

                    if self.__document_manager.save_chapter(project.chapter, self.__driver, project):
                        self.add_chapter_in_dict(project) 
                    
                    end_time_1 = time.time()

                    end_time = time.time()
                    
                    execution_time_1 = (end_time_1 - start_time_1)

                    execution_time = (end_time - start_time) - execution_time_1
                    
                    self.msg_manager.show_message('time_save', execution_time_1)

                    self.msg_manager.show_message('time_job', execution_time)

                elif not self.navigate_to_next_page(next_button_xpath, project):
                    break

            except Exception as e:
                self.msg_manager.show_message('there_was_an_error', e)
                break

        self.__document_manager.save_document()
        self.saved_chapters.clear()