class MessageManager:
    def __init__(self):
        self.messages = {
            'start':                        'Введите ссылку на проект или главу: ',
            'error_404':                    'Ошибка 404 для URL: {}',
            'invalid_url':                  'Невалидная ссылка на проект или главу.',
            'folder_creat':                 'Создана папка для проекта.',
            'next_or_exit':                 'Продолжить скачивать главы или выйти y/n',
            'invalid_input':                'Неверный ввод! Пожалуйста, введите "y" или "n".',
            'chapter_saved':                'Глава {} добавлена в документ.',
            'program_complete':             'Работа программы завершена.',
            'continue_or_exit':             'Продолжить скачивать проекты или выйти y/n: ',
            'download_complete':            'Скачивание завершено.',
            'there_was_an_error':           'Произошла ошибка: {}',
            'uploading_document':           'Загружаем существующий документ.',
            'document_not_found':           'Документ не найден. Создаём новый.',
            'html_chapter_saved':           'HTML код главы {} сохранен.',
            'folder_already_creat':         'Папка для проекта уже существует.',
            'special_symbol_found':         'Спец символ найден.',
            'project_opening_error':        'Произошла ошибка при открытии проекта: {}',
            'folder_creation_error':        'Ошибка при создании папки: {}',
            'chapter_already_saved':        'Глава {} уже сохранена',
            'all_chapters_are_saved_to':    'Все главы сохранены в файл: {}',
            'current_volume_and_chapter':   'Текущий том: {}, Текущая глава: {}',
            'time_spent':                   'Время, затраченное на сохранение главы {}: {:.2f} секунд',  # Обратите внимание на формат {:.2f}
        }

    def show_message(self, message_key, *format_args, inline=False):
        message = self.messages.get(message_key, "Неизвестное сообщение")
        
        if format_args:
            # Используем форматирование .format для каждого аргумента
            message = message.format(*format_args)
        
        if inline:
            print(message, end="")
        else:
            print(message)
