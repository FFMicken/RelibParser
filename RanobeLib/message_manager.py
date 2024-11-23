class MessageManager:
    def __init__(self):
        self.messages = {
            #document_manager
            'html_chapter_saved':           'HTML код главы {} сохранен.',
            'error_saving_in_format':       'Ошибка при сохранении в формате {}: {}',
            'current_volume_and_chapter':   'Текущий том: {}, Текущая глава: {}',
            'all_chapters_are_saved_to':    'Все главы сохранены в файл: {}',

            #handling_uirl
            'invalid_url':                  'Невалидная ссылка на проект или главу.',
            'folder_creat':                 'Создана папка для проекта.',
            'folder_already_creat':         'Папка уже существует',
            'folder_creation_error':        'Ошибка при создании папки: {}',
            'special_symbol_found':         'Спец символ найден.',

            #LibScraper
            'start':                        'Введите ссылку на проект или главу: ',
            'select_formats':               'В каких форматах вы хотите сохранить проект?:\n1. Docx\n2. PDF\n3. FB2\n4. EPUB\nНапишите цифры поряд через пробел: ',

            #novel_manager
            'error_404':                    'Ошибка 404 для URL: {}',
            'project_opening_error':        'Произошла ошибка при открытии проекта: {}',

            #web_driver_manager
            'continue_or_exit':             'Продолжить скачивать проекты или выйти y/n: ',
            'download_complete':            'Скачивание завершено.',
            'invalid_input':                'Неверный ввод! Пожалуйста, введите "y" или "n"',
            'error_clos_driver':            'Ошибка при закрытии драйвера: {}',

            #save_to
            'there_was_an_error':           'Произошла ошибка: {}',

        }

    def show_message(self, message_key, *format_args, inline=False):
        message = self.messages.get(message_key, f"Неизвестное сообщение: {message_key}")
            
        if format_args:
            message = message.format(*format_args)
        
        if inline:
            print(message, end="")
        else:
            print(message)
