import threading
import time
from datetime import datetime
from app.controllers.lembreteRecord import LembreteRecord
from app.controllers.websocketManager import websocket_manager
from app.controllers.dataRecord import DataRecord

class LembreteNotificationService:
    """Serviço de notificações para lembretes próximos do vencimento"""
    
    def __init__(self):
        self.is_running = False
        self.thread = None
        self.check_interval = 60  # Verificar a cada 1 minuto
        self.notification_window = 30  # Notificar 30 minutos antes
        self.data_record = DataRecord()
    
    def start(self):
        """Inicia o serviço de notificações"""
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._run_notification_loop, daemon=True)
            self.thread.start()
            print("🔔 Serviço de notificações de lembretes iniciado")
    
    def stop(self):
        """Para o serviço de notificações"""
        self.is_running = False
        if self.thread:
            self.thread.join()
        print("🔕 Serviço de notificações de lembretes parado")
    
    def _run_notification_loop(self):
        """Loop principal para verificar lembretes"""
        while self.is_running:
            try:
                self._check_all_users_reminders()
            except Exception as e:
                print(f"❌ Erro no serviço de notificações: {e}")
            
            # Aguardar antes da próxima verificação
            time.sleep(self.check_interval)
    
    def _check_all_users_reminders(self):
        """Verifica lembretes de todos os usuários ativos"""
        # Obter todos os usuários com sessões ativas
        active_users = self.data_record.get_active_users()
        
        for user_email in active_users:
            try:
                self._check_user_reminders(user_email)
            except Exception as e:
                print(f"❌ Erro ao verificar lembretes de {user_email}: {e}")
    
    def _check_user_reminders(self, user_email):
        """Verifica lembretes de um usuário específico"""
        lembrete_record = LembreteRecord(user_email)
        lembretes = lembrete_record.read()
        
        for i, lembrete in enumerate(lembretes):
            # Verificar se está próximo do vencimento e ainda não foi notificado
            if lembrete.is_due_soon(self.notification_window) and not lembrete.notified:
                self._send_reminder_notification(user_email, lembrete, i)
                lembrete_record.mark_as_notified(i)
            
            # Verificar se já venceu
            elif lembrete.is_expired() and not lembrete.notified:
                self._send_expired_notification(user_email, lembrete, i)
                lembrete_record.mark_as_notified(i)
    
    def _send_reminder_notification(self, user_email, lembrete, index):
        """Envia notificação de lembrete próximo ao vencimento"""
        notification_data = {
            'titulo': lembrete.titulo,
            'desc': lembrete.desc,
            'prazo': lembrete.get_formatted_prazo(),
            'time_remaining': lembrete.get_time_remaining(),
            'index': index,
            'type': 'due_soon'
        }
        
        websocket_manager.broadcast_to_user(
            user_email, 
            'lembrete_notification', 
            notification_data
        )
        
        print(f"🔔 Notificação enviada para {user_email}: {lembrete.titulo}")
    
    def _send_expired_notification(self, user_email, lembrete, index):
        """Envia notificação de lembrete vencido"""
        notification_data = {
            'titulo': lembrete.titulo,
            'desc': lembrete.desc,
            'prazo': lembrete.get_formatted_prazo(),
            'time_remaining': 'Vencido',
            'index': index,
            'type': 'expired'
        }
        
        websocket_manager.broadcast_to_user(
            user_email, 
            'lembrete_notification', 
            notification_data
        )
        
        print(f"⚠️ Notificação de vencimento enviada para {user_email}: {lembrete.titulo}")

# Instância global do serviço
notification_service = LembreteNotificationService()
