import json
import uuid
from threading import Lock
from datetime import datetime

class WebSocketManager:
    """
    Gerenciador de WebSocket para sincronização de dados entre dispositivos
    """
    
    def __init__(self):
        self.connections = {}  # {user_email: [websocket_connections]}
        self.user_sessions = {}  # {session_id: user_email}
        self.lock = Lock()
    
    def add_connection(self, websocket, user_email, session_id):
        """Adiciona uma nova conexão WebSocket para um usuário"""
        with self.lock:
            if user_email not in self.connections:
                self.connections[user_email] = []
            
            connection_data = {
                'websocket': websocket,
                'session_id': session_id,
                'connected_at': datetime.now().isoformat(),
                'connection_id': str(uuid.uuid4())
            }
            
            self.connections[user_email].append(connection_data)
            self.user_sessions[session_id] = user_email
            
            print(f"Nova conexão WebSocket para {user_email} (Session: {session_id})")
            return connection_data['connection_id']
    
    def remove_connection(self, websocket, user_email=None, session_id=None):
        """Remove uma conexão WebSocket"""
        with self.lock:
            if session_id and session_id in self.user_sessions:
                user_email = self.user_sessions[session_id]
                del self.user_sessions[session_id]
            
            if user_email and user_email in self.connections:
                self.connections[user_email] = [
                    conn for conn in self.connections[user_email]
                    if conn['websocket'] != websocket
                ]
                
                if not self.connections[user_email]:
                    del self.connections[user_email]
                
                print(f"Conexão WebSocket removida para {user_email}")
    
    def broadcast_to_user(self, user_email, message_type, data):
        """Envia uma mensagem para todas as conexões de um usuário específico"""
        if user_email not in self.connections:
            return
        
        message = {
            'type': message_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        message_json = json.dumps(message, ensure_ascii=False)
        
        # Lista de conexões para remover (conexões mortas)
        dead_connections = []
        
        with self.lock:
            for connection in self.connections[user_email][:]:  # Cópia da lista
                try:
                    websocket = connection['websocket']
                    websocket.send(message_json)
                except Exception as e:
                    print(f"Erro ao enviar mensagem WebSocket: {e}")
                    dead_connections.append(connection)
            
            # Remove conexões mortas
            for dead_conn in dead_connections:
                if dead_conn in self.connections[user_email]:
                    self.connections[user_email].remove(dead_conn)
                    if dead_conn['session_id'] in self.user_sessions:
                        del self.user_sessions[dead_conn['session_id']]
            
            # Remove lista vazia
            if user_email in self.connections and not self.connections[user_email]:
                del self.connections[user_email]
    
    def sync_lembrete_added(self, user_email, lembrete_data):
        """Sincroniza adição de lembrete"""
        self.broadcast_to_user(user_email, 'lembrete_added', lembrete_data)
    
    def sync_lembrete_deleted(self, user_email, index):
        """Sincroniza remoção de lembrete"""
        self.broadcast_to_user(user_email, 'lembrete_deleted', {'index': index})
    
    def sync_task_added(self, user_email, task_data):
        """Sincroniza adição de task"""
        self.broadcast_to_user(user_email, 'task_added', task_data)
    
    def sync_task_deleted(self, user_email, index):
        """Sincroniza remoção de task"""
        self.broadcast_to_user(user_email, 'task_deleted', {'index': index})
    
    def sync_timer_added(self, user_email, timer_data):
        """Sincroniza adição de timer"""
        self.broadcast_to_user(user_email, 'timer_added', timer_data)
    
    def sync_timer_deleted(self, user_email, index):
        """Sincroniza remoção de timer"""
        self.broadcast_to_user(user_email, 'timer_deleted', {'index': index})
    
    def get_user_connections_count(self, user_email):
        """Retorna o número de conexões ativas para um usuário"""
        return len(self.connections.get(user_email, []))
    
    def get_all_connections_count(self):
        """Retorna o número total de conexões ativas"""
        total = 0
        for connections in self.connections.values():
            total += len(connections)
        return total

# Instância global do gerenciador
websocket_manager = WebSocketManager()
