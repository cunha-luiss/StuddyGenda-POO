import json
import os
from app.models.timer import Timer

class TimerRecord:
    def __init__(self, user_email):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self._path = os.path.join(base_dir, 'db/timer', f'{user_email}_timers.json')
        os.makedirs(base_dir, exist_ok=True)
        if not os.path.exists(self._path):
            with open(self._path, 'w', encoding='utf-8') as f:
                json.dump([], f)
        self.read()

    def read(self):
        try:
            with open(self._path, "r", encoding='utf-8') as arquivo_json:
                timer_data = json.load(arquivo_json)
                self.__timers = [Timer(**data) for data in timer_data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.__timers = []
        return self.__timers

    def book(self, tempo):
        new_timer = Timer(tempo)
        self.__timers.append(new_timer)
        with open(self._path, "w", encoding='utf-8') as arquivo_json:
            timer_data = [vars(timer) for timer in self.__timers]
            json.dump(timer_data, arquivo_json, indent=4)

    def delete(self, index):
        if 0 <= index < len(self.__timers):
            del self.__timers[index]
            with open(self._path, "w", encoding='utf-8') as arquivo_json:
                timer_data = [vars(timer) for timer in self.__timers]
                json.dump(timer_data, arquivo_json, indent=4)