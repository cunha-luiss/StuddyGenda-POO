from datetime import datetime, timedelta
import json

class Lembrete:
    def __init__(self, titulo, desc, prazo, created_at=None, notified=False):
        self.titulo = titulo
        self.desc = desc
        self.prazo = prazo  # ISO format datetime string
        self.created_at = created_at or datetime.now().isoformat()
        self.notified = notified  # Flag para controlar se já foi notificado
    
    def get_prazo_datetime(self):
        """Converte o prazo string para objeto datetime"""
        try:
            return datetime.fromisoformat(self.prazo.replace('Z', '+00:00'))
        except:
            # Tentar formato antigo se falhar
            try:
                return datetime.strptime(self.prazo, '%Y-%m-%d %H:%M:%S')
            except:
                return datetime.now()
    
    def is_expired(self):
        """Verifica se o lembrete já venceu"""
        return self.get_prazo_datetime() < datetime.now()
    
    def is_due_soon(self, minutes=30):
        """Verifica se o lembrete está próximo do vencimento"""
        prazo_dt = self.get_prazo_datetime()
        now = datetime.now()
        return now <= prazo_dt <= now + timedelta(minutes=minutes)
    
    def get_time_remaining(self):
        """Retorna o tempo restante até o vencimento"""
        prazo_dt = self.get_prazo_datetime()
        now = datetime.now()
        
        if prazo_dt < now:
            return "Vencido"
        
        diff = prazo_dt - now
        
        if diff.days > 0:
            return f"{diff.days} dias"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} horas"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minutos"
        else:
            return "Menos de 1 minuto"
    
    def get_formatted_prazo(self):
        """Retorna o prazo formatado para exibição"""
        try:
            dt = self.get_prazo_datetime()
            return dt.strftime('%d/%m/%Y às %H:%M')
        except:
            return self.prazo
    
    def to_dict(self):
        """Converte o lembrete para dicionário"""
        return {
            'titulo': self.titulo,
            'desc': self.desc,
            'prazo': self.prazo,
            'created_at': self.created_at,
            'notified': self.notified
        }