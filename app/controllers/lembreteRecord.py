import json
import os
from app.models.lembrete import Lembrete

class LembreteRecord:
    def __init__(self, user_email):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self._path = os.path.join(base_dir, 'db/lembrete', f'{user_email}_lembretes.json')
        if not os.path.exists(self._path):
            with open(self._path, 'w', encoding='utf-8') as f:
                json.dump([], f)
        self.read()

    def read(self):
        try:
            with open(self._path, "r", encoding='utf-8') as arquivo_json:
                lembrete_data = json.load(arquivo_json)
                self.__lembretes = [Lembrete(**data) for data in lembrete_data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.__lembretes = []
        return self.__lembretes

    def book(self, titulo, desc, prazo):
        new_lembrete = Lembrete(titulo, desc, prazo)
        self.__lembretes.append(new_lembrete)
        with open(self._path, "w", encoding='utf-8') as arquivo_json:
            lembrete_data = [vars(lembrete) for lembrete in self.__lembretes]
            json.dump(lembrete_data, arquivo_json, indent=4, ensure_ascii=False)

    def delete(self, index):
        if 0 <= index < len(self.__lembretes):
            del self.__lembretes[index]
            with open(self._path, "w", encoding='utf-8') as arquivo_json:
                lembrete_data = [vars(lembrete) for lembrete in self.__lembretes]
                json.dump(lembrete_data, arquivo_json, indent=4, ensure_ascii=False)