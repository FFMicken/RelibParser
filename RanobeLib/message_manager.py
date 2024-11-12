class MessageManager:
    def __init__(self):
        self.messages = {
            'start':                        'Введите ссылку на проект или главу: ',
            'error_404':                    'Ошибка 404 для URL: {}',
            'time_spent':                   'Время, затраченное на сохранение главы {}: {:.2f} секунд.',
            'invalid_url':                  'Невалидная ссылка на проект или главу.',
            'folder_creat':                 'Создана папка для проекта.',
            'next_or_exit':                 'Продолжить скачивать главы или выйти y/n',
            'invalid_input':                'Неверный ввод! Пожалуйста, введите "y" или "n"',
            'select_formats':               'В каких форматах вы хотите сохранить проект?:\n1. Docx\n2. PDF\n3. FB2\n4. EPUB\nНапишите цифры поряд через пробел: ',
            'program_complete':             'Работа программы завершена.',
            'continue_or_exit':             'Продолжить скачивать проекты или выйти y/n: ',
            'download_complete':            'Скачивание завершено.',
            'there_was_an_error':           'Произошла ошибка: {}',
            'html_chapter_saved':           'HTML код главы {} сохранен.',
            'special_symbol_found':         'Спец символ найден.',
            'project_opening_error':        'Произошла ошибка при открытии проекта: {}',
            'folder_creation_error':        'Ошибка при создании папки: {}',
            'error_saving_in_format':       'Ошибка при сохранении в формате {}: {}',
            'all_chapters_are_saved_to':    'Все главы сохранены в файл: {}',
            'current_volume_and_chapter':   'Текущий том: {}, Текущая глава: {}',

            'chapter_does_not_text':        'Глава {} не содержит текста.',

        }

    def show_message(self, message_key, *format_args, inline=False):
        message = self.messages.get(message_key, "Неизвестное сообщение")
            
        if format_args:
            message = message.format(*format_args)
        
        if inline:
            print(message, end="")
        else:
            print(message)
