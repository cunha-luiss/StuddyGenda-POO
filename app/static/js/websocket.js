/**
 * Gerenciador de WebSocket para sincronização em tempo real
 */
class WebSocketSync {
    constructor() {
        this.socket = null;
        this.connectionId = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectInterval = 3000; // 3 segundos
        this.isConnected = false;
        this.heartbeatInterval = null;
        
        this.init();
    }
    
    init() {
        this.connect();
        this.setupHeartbeat();
    }
    
    connect() {
        try {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/websocket`;
            
            this.socket = new WebSocket(wsUrl);
            
            this.socket.onopen = (event) => {
                console.log('✅ WebSocket conectado');
                this.isConnected = true;
                this.reconnectAttempts = 0;
                this.showConnectionStatus('connected');
            };
            
            this.socket.onmessage = (event) => {
                try {
                    const message = JSON.parse(event.data);
                    this.handleMessage(message);
                } catch (error) {
                    console.error('❌ Erro ao processar mensagem WebSocket:', error);
                }
            };
            
            this.socket.onclose = (event) => {
                console.log('🔌 WebSocket desconectado');
                this.isConnected = false;
                this.showConnectionStatus('disconnected');
                
                if (this.reconnectAttempts < this.maxReconnectAttempts) {
                    this.scheduleReconnect();
                }
            };
            
            this.socket.onerror = (error) => {
                console.error('❌ Erro WebSocket:', error);
                this.showConnectionStatus('error');
            };
            
        } catch (error) {
            console.error('❌ Erro ao conectar WebSocket:', error);
            this.scheduleReconnect();
        }
    }
    
    scheduleReconnect() {
        this.reconnectAttempts++;
        console.log(`🔄 Tentando reconectar WebSocket (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
        
        setTimeout(() => {
            this.connect();
        }, this.reconnectInterval * this.reconnectAttempts);
    }
    
    setupHeartbeat() {
        // Enviar ping a cada 30 segundos para manter conexão viva
        this.heartbeatInterval = setInterval(() => {
            if (this.isConnected && this.socket && this.socket.readyState === WebSocket.OPEN) {
                this.send('ping', {});
            }
        }, 30000);
    }
    
    send(type, data) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            const message = {
                type: type,
                data: data,
                timestamp: new Date().toISOString()
            };
            this.socket.send(JSON.stringify(message));
        }
    }
    
    handleMessage(message) {
        console.log('📨 Mensagem WebSocket recebida:', message);
        
        switch (message.type) {
            case 'connection_established':
                this.connectionId = message.data.connection_id;
                this.showDeviceCount(message.data.connected_devices);
                break;
                
            case 'lembrete_added':
                this.handleLembreteAdded(message.data);
                break;
                
            case 'lembrete_deleted':
                this.handleLembreteDeleted(message.data);
                break;
                
            case 'task_added':
                this.handleTaskAdded(message.data);
                break;
                
            case 'task_deleted':
                this.handleTaskDeleted(message.data);
                break;
                
            case 'timer_added':
                this.handleTimerAdded(message.data);
                break;
                
            case 'timer_deleted':
                this.handleTimerDeleted(message.data);
                break;
                
            case 'pong':
                // Resposta do heartbeat - conexão está viva
                break;
                
            default:
                console.log('🤔 Tipo de mensagem desconhecido:', message.type);
        }
    }
    
    handleLembreteAdded(data) {
        this.showSyncNotification('Novo lembrete adicionado em outro dispositivo');
        // Recarregar lembretes ou adicionar dinamicamente
        this.refreshLembretes();
    }
    
    handleLembreteDeleted(data) {
        this.showSyncNotification('Lembrete removido em outro dispositivo');
        this.refreshLembretes();
    }
    
    handleTaskAdded(data) {
        this.showSyncNotification('Nova tarefa adicionada em outro dispositivo');
        this.refreshTasks();
    }
    
    handleTaskDeleted(data) {
        this.showSyncNotification('Tarefa removida em outro dispositivo');
        this.refreshTasks();
    }
    
    handleTimerAdded(data) {
        this.showSyncNotification('Novo timer adicionado em outro dispositivo');
        this.refreshTimers();
    }
    
    handleTimerDeleted(data) {
        this.showSyncNotification('Timer removido em outro dispositivo');
        this.refreshTimers();
    }
    
    refreshLembretes() {
        // Recarregar dados de lembretes
        window.location.reload();
    }
    
    refreshTasks() {
        // Recarregar dados de tasks
        window.location.reload();
    }
    
    refreshTimers() {
        // Recarregar dados de timers
        window.location.reload();
    }
    
    showConnectionStatus(status) {
        const statusElement = document.getElementById('websocket-status');
        if (!statusElement) {
            this.createStatusElement();
            return this.showConnectionStatus(status);
        }
        
        statusElement.className = `websocket-status ${status}`;
        
        const messages = {
            connected: '🟢 Sincronizado',
            disconnected: '🔴 Desconectado',
            error: '⚠️ Erro de conexão'
        };
        
        statusElement.textContent = messages[status] || status;
        
        // Auto-ocultar status positivo após alguns segundos
        if (status === 'connected') {
            setTimeout(() => {
                statusElement.style.opacity = '0.7';
            }, 3000);
        }
    }
    
    showDeviceCount(count) {
        const countElement = document.getElementById('device-count');
        if (countElement) {
            countElement.textContent = count > 1 ? `${count} dispositivos conectados` : '1 dispositivo conectado';
        }
    }
    
    showSyncNotification(message) {
        // Criar notificação temporária
        const notification = document.createElement('div');
        notification.className = 'sync-notification';
        notification.innerHTML = `
            <i class="fas fa-sync"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(notification);
        
        // Mostrar animação
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        // Remover após alguns segundos
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 4000);
    }
    
    createStatusElement() {
        // Criar elemento de status se não existir
        const statusElement = document.createElement('div');
        statusElement.id = 'websocket-status';
        statusElement.className = 'websocket-status';
        
        const headerControls = document.querySelector('.header-controls');
        if (headerControls) {
            headerControls.insertBefore(statusElement, headerControls.firstChild);
        }
    }
    
    disconnect() {
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
        }
        
        if (this.socket) {
            this.socket.close();
        }
    }
}

// Inicializar WebSocket quando a página carregar
let websocketSync = null;

document.addEventListener('DOMContentLoaded', function() {
    // Verificar se estamos na página da aplicação
    if (window.location.pathname === '/appGenda') {
        websocketSync = new WebSocketSync();
    }
});

// Limpar conexões quando sair da página
window.addEventListener('beforeunload', function() {
    if (websocketSync) {
        websocketSync.disconnect();
    }
});
