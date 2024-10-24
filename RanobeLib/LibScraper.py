from handling_url import UrlCreate
from novel_manager import NovelManager
from message_manager import MessageManager
from document_manager import DocumentManager
from web_driver_manager import WebDriverManager

def main():
    while True:
        # Создаем объект для управления сообщениями
        msg_manager = MessageManager()
        
        # Выводим сообщение с указанием, что ввод будет в той же строке (inline=True)
        msg_manager.show_message('start', inline=True)

        # Получаем ссылку на проект от пользователя
        project_url = input("")
        
        try:
            # Создаём объект проекта с переданной ссылкой
            project = UrlCreate(project_url, msg_manager)

            # Получаем данные о проекте
            project.give_project()

            if not hasattr(project, 'name_project'):  # Если атрибут не существует, значит проект не был создан
                continue

        except ValueError:
            # Выводим сообщение об ошибке и возвращаемся в начало цикла
            msg_manager.show_message('invalid_url')
            continue
        
        # Создаем объект драйвер
        web_driver_manager = WebDriverManager(msg_manager)

        # Создаем объект документ
        document_manager = DocumentManager(project.project_dir, project.name_project, msg_manager)
        
        # Создаем объект Менеджер глав
        chapter_manager = NovelManager(web_driver_manager.get_driver(), document_manager, msg_manager)

        # Открываем главы
        chapter_manager.open_project_or_chapters(project)

        # Завершаем программу, если пользователь выбрал "n"
        if not web_driver_manager.next_or_exit():
            exit()


# Запуск основной функции
if __name__ == '__main__':
    main()
