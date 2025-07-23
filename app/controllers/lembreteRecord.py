import json
import os
from datetime import datetime
from app.models.lembrete import Lembrete

class LembreteRecord:
    def __init__(self, user_email):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self._path = os.path.join(base_dir, 'db/lembrete', f'{user_email}_lembretes.json')

        db_dir = os.path.dirname(self._path)
        os.makedirs(db_dir, exist_ok=True)
        
        if not os.path.exists(self._path):
            with open(self._path, 'w', encoding='utf-8') as f:
                json.dump([], f)
        self.read()

    def read(self):
        try:
            with open(self._path, "r", encoding='utf-8') as arquivo_json:
                lembrete_data = json.load(arquivo_json)
                self.__lembretes = []
                for data in lembrete_data:
                    # Compatibilidade com formato antigo
                    if isinstance(data, dict):
                        self.__lembretes.append(Lembrete(**data))
                    else:
                        # Formato antigo sem dicionário
                        self.__lembretes.append(Lembrete(data.get('titulo', ''), data.get('desc', ''), data.get('prazo', '')))
        except (FileNotFoundError, json.JSONDecodeError):
            self.__lembretes = []
        return self.__lembretes

    def book(self, titulo, desc, prazo_datetime):
        """
        Adiciona um novo lembrete
        prazo_datetime: objeto datetime ou string ISO
        """
        if isinstance(prazo_datetime, datetime):
            prazo_str = prazo_datetime.isoformat()
        else:
            prazo_str = prazo_datetime
            
        new_lembrete = Lembrete(titulo, desc, prazo_str)
        self.__lembretes.append(new_lembrete)
        self._save()

    def delete(self, index):
        if 0 <= index < len(self.__lembretes):
            del self.__lembretes[index]
            self._save()

    def get_due_soon(self, minutes=30):
        """Retorna lembretes que estão próximos do vencimento"""
        return [lembrete for lembrete in self.__lembretes if lembrete.is_due_soon(minutes) and not lembrete.notified]
    
    def get_expired(self):
        """Retorna lembretes vencidos"""
        return [lembrete for lembrete in self.__lembretes if lembrete.is_expired()]
    
    def mark_as_notified(self, lembrete_index):
        """Marca um lembrete como já notificado"""
        if 0 <= lembrete_index < len(self.__lembretes):
            self.__lembretes[lembrete_index].notified = True
            self._save()
    
    def _save(self):
        """Salva os lembretes no arquivo JSON"""
        with open(self._path, "w", encoding='utf-8') as arquivo_json:
            lembrete_data = [lembrete.to_dict() for lembrete in self.__lembretes]
            json.dump(lembrete_data, arquivo_json, indent=4, ensure_ascii=False)