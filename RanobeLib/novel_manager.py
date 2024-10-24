from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NovelManager:
    def __init__(self, driver, document_manager, msg_manager):
        # Инициализация необходимых объектов и переменных
        self.__driver = driver
        self.__document_manager = document_manager
        self.msg_manager = msg_manager
        self.html_code = None
        self.timeout = 50

    def open_project_or_chapters(self, project):
        # Открытие проекта или глав в зависимости от наличия тома и главы
        if project.volume is None and project.chapter is None:
            self.open_first_chapter(project)  # Если нет тома и главы, открыть страницу проекта
        else:
            # Формирование ссылки для конкретного тома и главы
            url_template = f"https://ranobelib.me/ru/{project.project_id}--{project.original_name_project}/read/v{project.volume}/c{project.chapter}"
            self.open_chapters(project, url_template)  # Открыть главы

    def open_first_chapter(self, project):
        # Открытие страницы проекта
        url_template = f"https://ranobelib.me/ru/book/{project.project_id}--{project.original_name_project}?section=info"
        self.__driver.get(url_template)  # Переход по ссылке

        try:
            # Поиск и клик по кнопке для начала чтения первой главы
            project_link = f"/ru/{project.project_id}--{project.original_name_project}/read/v01/c01"
            self.click_element(By.XPATH, f"//a[@href='{project_link}' and contains(@class, 'btn') and contains(@class, 'is-filled') and contains(@class, 'variant-primary')]")

            # Ожидание загрузки первой главы
            WebDriverWait(self.__driver, self.timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))

            # Сохранение HTML, если есть спец символ
            if project.is_special:
                # Получение HTML-кода страницы
                self.html_code = self.__driver.page_source
                self.save_html("project_page.html")
            
            # Получение текущей URL страницы
            url_template = self.__driver.current_url

            # Разбор URL и обновление данных о проекте
            project.project_id, project.original_name_project, project.volume, project.chapter = project.parse_url(url_template)

            self.open_project_or_chapters(project)
            
        except Exception as e:
            # Логирование ошибки при открытии проекта
            self.log_error('project_opening_error', e)

    def open_chapters(self, project, url_template):
        # Открытие и обработка всех глав проекта
        while True:
            try:
                # Ожидание полной загрузки страницы
                WebDriverWait(self.__driver, self.timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                
                # Проверка на наличие 404 ошибки
                if "404" in self.__driver.current_url:
                    self.msg_manager.show_message('error_404', url_template)
                    break

                self.update_project_info(project)

                # Сохранение текущей главы
                self.__document_manager.save_chapters(project.chapter, self.__document_manager.doc, self.__driver, project)

                # Проверка наличия кнопки "Вперёд" — переход к следующей главе
                if self.navigate_to_next_page("//span[text()='Вперёд']", project):
                    continue

                # Если кнопки "Вперёд" нет, проверяем кнопку "К Тайтлу"
                if self.navigate_to_next_page("//span[text()='К Тайтлу']", project):
                    break
                
                # Если ни одной кнопки нет, завершаем цикл
                self.msg_manager.show_message('last_chapter_reached', project.chapter)
                break

            except Exception as e:
                # Логирование ошибки, если возникла ошибка во время обработки глав
                self.log_error('there_was_an_error', e)
                break

        # Сохранение документа после завершения обработки всех глав
        self.__document_manager.save_document()

    def update_project_info(self, project):
        # Получение текущей URL страницы
        url_template = self.__driver.current_url

        # Регулярное выражение для извлечения volume и chapter из URL
        match = project.check_chapter_and_volume(url_template)
        if match:
            project.volume = match.group(1)
            project.chapter = match.group(2)

        self.msg_manager.show_message('current_volume_and_chapter', project.volume, project.chapter)

    def click_element(self, by, value):
        # Клик по элементу, используя JavaScript, с ожиданием его доступности
        element = WebDriverWait(self.__driver, self.timeout).until(EC.element_to_be_clickable((by, value)))
        self.__driver.execute_script("arguments[0].click();", element)

    def navigate_to_next_page(self, xpath, project):
        # Проверка наличия элемента по XPATH (кнопка "Вперёд" или "К Тайтлу")
        buttons = self.__driver.find_elements(By.XPATH, xpath)
        if buttons:
            # Если кнопка найдена, кликаем по ней
            self.__driver.execute_script("arguments[0].click();", buttons[0])
            project.is_special = False
            return True
        return False

    def save_html(self, filename):
        # Сохранение HTML-кода страницы в файл
        with open(filename, "w", encoding="utf-8") as file:
            file.write(self.html_code)

    def log_error(self, error_type, exception):
        # Логирование ошибки и отображение сообщения пользователю
        self.msg_manager.show_message(error_type, exception)