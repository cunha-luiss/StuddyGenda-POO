from datetime import datetime, timedelta
import json
import sys
import os

# Adicionar o caminho do controllers para import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'controllers'))

try:
    from app.controllers.timezoneHelper import timezone_helper
except ImportError:
    # Fallback se não conseguir importar
    print("⚠️ TimezoneHelper não disponível, usando datetime padrão")
    
    class FallbackTimezoneHelper:
        def get_local_now(self):
            return datetime.now()
        
        def localize_datetime(self, dt_string):
            try:
                return datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
            except:
                return datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S')
        
        def to_local_string(self, dt):
            return dt.strftime('%d/%m/%Y às %H:%M')
        
        def to_utc_isoformat(self, dt):
            return dt.isoformat()
    
    timezone_helper = FallbackTimezoneHelper()

class Lembrete:
    def __init__(self, titulo, desc, prazo, created_at=None, notified=False):
        self.titulo = titulo
        self.desc = desc
        self.prazo = prazo  # UTC ISO format datetime string para armazenamento
        self.created_at = created_at or timezone_helper.to_utc_isoformat(timezone_helper.get_local_now())
        self.notified = notified  # Flag para controlar se já foi notificado
    
    def get_prazo_datetime(self):
        """Converte o prazo string para objeto datetime local"""
        try:
            return timezone_helper.localize_datetime(self.prazo)
        except Exception as e:
            print(f"❌ Erro ao converter prazo: {e}")
            return timezone_helper.get_local_now()
    
    def is_expired(self):
        """Verifica se o lembrete já venceu"""
        prazo_local = self.get_prazo_datetime()
        now_local = timezone_helper.get_local_now()
        return prazo_local < now_local
    
    def is_due_soon(self, minutes=30):
        """Verifica se o lembrete está próximo do vencimento"""
        prazo_local = self.get_prazo_datetime()
        now_local = timezone_helper.get_local_now()
        return now_local <= prazo_local <= now_local + timedelta(minutes=minutes)
    
    def get_time_remaining(self):
        """Retorna o tempo restante até o vencimento"""
        prazo_local = self.get_prazo_datetime()
        now_local = timezone_helper.get_local_now()
        
        if prazo_local < now_local:
            return "Vencido"
        
        diff = prazo_local - now_local
        
        if diff.days > 0:
            return f"{diff.days} dia{'s' if diff.days != 1 else ''}"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hora{'s' if hours != 1 else ''}"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minuto{'s' if minutes != 1 else ''}"
        else:
            return "Menos de 1 minuto"
    
    def get_formatted_prazo(self):
        """Retorna o prazo formatado para exibição no timezone local"""
        try:
            prazo_local = self.get_prazo_datetime()
            return timezone_helper.to_local_string(prazo_local)
        except Exception as e:
            print(f"❌ Erro ao formatar prazo: {e}")
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