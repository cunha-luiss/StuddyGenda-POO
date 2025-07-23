import json
import os
from app.models.task import Task

class TaskRecord:
    def __init__(self, user_email):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self._path = os.path.join(base_dir, 'db/task', f'{user_email}_tasks.json')

        db_dir = os.path.dirname(self._path)
        os.makedirs(db_dir, exist_ok=True)
        
        if not os.path.exists(self._path):
            with open(self._path, 'w', encoding='utf-8') as f:
                json.dump([], f)
        self.read()

    def read(self):
        try:
            with open(self._path, "r", encoding='utf-8') as arquivo_json:
                task_data = json.load(arquivo_json)
                self.__tasks = [Task(**data) for data in task_data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.__tasks = []
        return self.__tasks

    def book(self, nome, prioridade):
        new_task = Task(nome, prioridade)
        self.__tasks.append(new_task)
        with open(self._path, "w", encoding='utf-8') as arquivo_json:
            task_data = [vars(task) for task in self.__tasks]
            json.dump(task_data, arquivo_json, indent=4, ensure_ascii=False)

    def delete(self, index):
        if 0 <= index < len(self.__tasks):
            del self.__tasks[index]
            with open(self._path, "w", encoding='utf-8') as arquivo_json:
                task_data = [vars(task) for task in self.__tasks]
                json.dump(task_data, arquivo_json, indent=4, ensure_ascii=False)