import time

class TimerManager:
    def __init__(self):
        self.timers = {}

    def start(self, timer_name):
        if timer_name not in self.timers:
            self.timers[timer_name] = []
            
        self.timers[timer_name].append({'start': time.time(), 'end': None})

    def stop(self, timer_name):
        if timer_name in self.timers and self.timers[timer_name]:
            for entry in self.timers[timer_name]:
                if entry['end'] is None:
                    entry['end'] = time.time()
                    break

    def get_elapsed_time(self, timer_name):
        elapsed_time = 0

        for entry in self.timers[timer_name]:
            if entry['end'] is not None:
                elapsed_time += entry['end'] - entry['start']

        return elapsed_time

    def reset(self, timer_name):
        if timer_name in self.timers:
            self.timers[timer_name] = []

    def reset_all(self):
        self.timers = {}

    def print_elapsed_time(self, timer_name):
        try:
            elapsed_time = self.get_elapsed_time(timer_name)
            print(f"Таймер '{timer_name}': {elapsed_time:.2f} секунд")
        except ValueError as e:
            print(e)


#### Пример
# tm = TimerManager()

# # Измерение времени для первого элемента
# tm.start("element_1")
# time.sleep(1)  # Эмуляция работы
# tm.stop("element_1")

# # Измерение времени для второго элемента
# tm.start("element_2")
# time.sleep(2)  # Эмуляция работы
# tm.stop("element_2")

# # Повторное измерение для первого элемента
# tm.start("element_1")
# time.sleep(0.5)  # Эмуляция работы
# tm.stop("element_1")

# # Вывод времени для элементов
# tm.print_elapsed_time("element_1")  # Таймер 'element_1': 1.50 секунд
# tm.print_elapsed_time("element_2")  # Таймер 'element_2': 2.00 секунд

# # Сброс и повторный вывод
# tm.reset("element_1")
# tm.print_elapsed_time("element_1")  # Таймер 'element_1': 0.00 секунд
