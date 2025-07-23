"""
Utilitário para gerenciamento consistente de timezone
"""
import os
import platform
from datetime import datetime, timezone
import pytz

class TimezoneHelper:
    """Classe para gerenciar timezone de forma consistente entre sistemas operacionais"""
    
    def __init__(self):
        self._local_timezone = self._detect_local_timezone()
    
    def _detect_local_timezone(self):
        """Detecta o timezone local do sistema de forma robusta"""
        try:
            # Método 1: Tentar obter timezone do sistema
            if hasattr(datetime.now(), 'astimezone'):
                local_tz = datetime.now().astimezone().tzinfo
                if local_tz:
                    return local_tz
            
            # Método 2: Usar variáveis de ambiente (Unix/Linux)
            if platform.system() != 'Windows':
                tz_env = os.environ.get('TZ')
                if tz_env:
                    try:
                        return pytz.timezone(tz_env)
                    except:
                        pass
            
            # Método 3: Tentar detectar via pytz baseado na plataforma
            system = platform.system().lower()
            
            if system == 'windows':
                # Para Windows, tentar algumas opções comuns
                try:
                    import time
                    # Obter offset do sistema
                    offset_seconds = -time.timezone
                    if time.daylight:
                        offset_seconds += 3600
                    
                    # Criar timezone com offset
                    offset_hours = offset_seconds // 3600
                    offset_minutes = (abs(offset_seconds) % 3600) // 60
                    
                    if offset_hours >= 0:
                        tz_name = f"Etc/GMT-{offset_hours}"
                    else:
                        tz_name = f"Etc/GMT+{abs(offset_hours)}"
                    
                    return pytz.timezone(tz_name)
                except:
                    pass
            
            # Método 4: Fallback para UTC
            print("⚠️ Não foi possível detectar timezone local. Usando UTC.")
            return pytz.UTC
            
        except Exception as e:
            print(f"❌ Erro ao detectar timezone: {e}. Usando UTC.")
            return pytz.UTC
    
    def get_local_now(self):
        """Retorna datetime atual no timezone local"""
        try:
            return datetime.now(self._local_timezone)
        except:
            # Fallback para datetime sem timezone
            return datetime.now()
    
    def localize_datetime(self, dt_string):
        """Converte string datetime para datetime local"""
        try:
            # Se já tem timezone info
            if 'T' in dt_string and ('+' in dt_string or 'Z' in dt_string):
                dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
                return dt.astimezone(self._local_timezone)
            
            # Se não tem timezone, assumir que é local
            if 'T' in dt_string:
                dt = datetime.fromisoformat(dt_string)
            else:
                # Formato de data/hora simples
                dt = datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S')
            
            # Localizar o datetime
            if hasattr(self._local_timezone, 'localize'):
                return self._local_timezone.localize(dt)
            else:
                return dt.replace(tzinfo=self._local_timezone)
                
        except Exception as e:
            print(f"❌ Erro ao localizar datetime {dt_string}: {e}")
            return datetime.now()
    
    def to_local_string(self, dt):
        """Converte datetime para string no formato local"""
        try:
            if dt.tzinfo is None:
                # Se não tem timezone, assumir local
                if hasattr(self._local_timezone, 'localize'):
                    dt = self._local_timezone.localize(dt)
                else:
                    dt = dt.replace(tzinfo=self._local_timezone)
            else:
                # Converter para timezone local
                dt = dt.astimezone(self._local_timezone)
            
            return dt.strftime('%d/%m/%Y às %H:%M')
        except Exception as e:
            print(f"❌ Erro ao formatar datetime: {e}")
            return str(dt)
    
    def create_local_datetime(self, date_str, time_str):
        """Cria datetime local a partir de strings de data e hora"""
        try:
            # Combinar data e hora
            datetime_str = f"{date_str} {time_str}"
            dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            
            # Localizar no timezone correto
            if hasattr(self._local_timezone, 'localize'):
                local_dt = self._local_timezone.localize(dt)
            else:
                local_dt = dt.replace(tzinfo=self._local_timezone)
            
            return local_dt
            
        except Exception as e:
            print(f"❌ Erro ao criar datetime local: {e}")
            return datetime.now()
    
    def to_utc_isoformat(self, dt):
        """Converte datetime para UTC ISO format para armazenamento"""
        try:
            if dt.tzinfo is None:
                # Se não tem timezone, assumir local
                if hasattr(self._local_timezone, 'localize'):
                    dt = self._local_timezone.localize(dt)
                else:
                    dt = dt.replace(tzinfo=self._local_timezone)
            
            # Converter para UTC
            utc_dt = dt.astimezone(pytz.UTC)
            return utc_dt.isoformat()
            
        except Exception as e:
            print(f"❌ Erro ao converter para UTC: {e}")
            return dt.isoformat()
    
    def get_timezone_info(self):
        """Retorna informações sobre o timezone detectado"""
        local_now = self.get_local_now()
        return {
            'timezone': str(self._local_timezone),
            'current_time': local_now.strftime('%Y-%m-%d %H:%M:%S %Z'),
            'utc_offset': local_now.strftime('%z'),
            'platform': platform.system(),
            'is_dst': local_now.dst() is not None and local_now.dst().total_seconds() > 0
        }

# Instância global do helper
timezone_helper = TimezoneHelper()
