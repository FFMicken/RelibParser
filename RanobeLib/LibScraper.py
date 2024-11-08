from handling_url import UrlCreate
from novel_manager import NovelManager
from message_manager import MessageManager
from document_manager import DocumentManager
from web_driver_manager import WebDriverManager

def main():
    while True:
        msg_manager = MessageManager()
        
        msg_manager.show_message('start', inline=True)

        project_url = input()
        
        try:
            project = UrlCreate(project_url, msg_manager)

            project.give_project()

            if not hasattr(project, 'name_project'):
                continue

        except ValueError:
            msg_manager.show_message('invalid_url')
            continue
        
        msg_manager.show_message('select_formats')

        formats = input().split()
        
        web_driver_manager = WebDriverManager(msg_manager)

        document_manager = DocumentManager(project.project_dir, project.name_project, msg_manager, formats)
        
        chapter_manager = NovelManager(web_driver_manager.get_driver(), document_manager, msg_manager)

        chapter_manager.open_project_or_chapters(project)

        if not web_driver_manager.next_or_exit():
            exit()

if __name__ == '__main__':
    main()
