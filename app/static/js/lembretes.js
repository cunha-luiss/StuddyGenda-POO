/**
 * Script para funcionalidades específicas de lembretes
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeLembreteFeatures();
    updateLembreteTimers();
    detectClientTimezone();
    
    // Atualizar timers a cada minuto
    setInterval(updateLembreteTimers, 60000);
});

function detectClientTimezone() {
    try {
        // Detectar timezone do navegador
        const clientTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        const offset = new Date().getTimezoneOffset();
        
        // Enviar informação para o servidor se necessário
        const timezoneInfo = {
            timezone: clientTimezone,
            offset: offset,
            offsetString: new Date().toString().match(/([A-Z]{3,4}[+-]\d{4})/)?.[1] || 'Unknown'
        };
        
        // Armazenar no localStorage para uso futuro
        localStorage.setItem('clientTimezone', JSON.stringify(timezoneInfo));
        
        console.log('🌍 Timezone detectado:', timezoneInfo);
        
    } catch (error) {
        console.warn('⚠️ Não foi possível detectar timezone do cliente:', error);
    }
}

function initializeLembreteFeatures() {
    // Configurar valores padrão para inputs de data/hora
    setDefaultDateTime();
    
    // Adicionar validação de formulário
    const lembreteForm = document.querySelector('#lembretes form');
    if (lembreteForm) {
        lembreteForm.addEventListener('submit', validateLembreteForm);
    }
}

function setDefaultDateTime() {
    const dateInput = document.querySelector('input[name="prazo_date"]');
    const timeInput = document.querySelector('input[name="prazo_time"]');
    
    if (dateInput && timeInput) {
        // Usar timezone do cliente para definir valores padrão
        const now = new Date();
        const tomorrow = new Date(now);
        tomorrow.setDate(tomorrow.getDate() + 1);
        
        // Definir data padrão como amanhã
        const year = tomorrow.getFullYear();
        const month = String(tomorrow.getMonth() + 1).padStart(2, '0');
        const day = String(tomorrow.getDate()).padStart(2, '0');
        dateInput.value = `${year}-${month}-${day}`;
        
        // Definir hora padrão como 9:00
        timeInput.value = '09:00';
        
        // Validar que a data não seja no passado (usando timezone local)
        dateInput.addEventListener('change', function() {
            const selectedDate = new Date(this.value + 'T00:00:00');
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            if (selectedDate < today) {
                const todayStr = today.toISOString().split('T')[0];
                this.value = todayStr;
                showToast('⚠️ A data não pode ser no passado', 'warning');
            }
        });
        
        // Validar hora se for hoje (usando timezone local)
        timeInput.addEventListener('change', function() {
            const selectedDate = new Date(dateInput.value + 'T00:00:00');
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            if (selectedDate.getTime() === today.getTime()) {
                const [hours, minutes] = this.value.split(':');
                const selectedTime = new Date();
                selectedTime.setHours(parseInt(hours), parseInt(minutes), 0, 0);
                
                const now = new Date();
                if (selectedTime <= now) {
                    const futureTime = new Date(now.getTime() + 60 * 60 * 1000); // +1 hora
                    const futureHours = String(futureTime.getHours()).padStart(2, '0');
                    const futureMinutes = String(futureTime.getMinutes()).padStart(2, '0');
                    this.value = `${futureHours}:${futureMinutes}`;
                    showToast('⚠️ O horário deve ser no futuro', 'warning');
                }
            }
        });
    }
}

function validateLembreteForm(event) {
    const titulo = document.querySelector('input[name="titulo"]');
    const dateInput = document.querySelector('input[name="prazo_date"]');
    const timeInput = document.querySelector('input[name="prazo_time"]');
    
    // Validar título
    if (!titulo.value.trim()) {
        event.preventDefault();
        showToast('❌ Título é obrigatório', 'error');
        titulo.focus();
        return false;
    }
    
    // Validar data e hora
    if (!dateInput.value || !timeInput.value) {
        event.preventDefault();
        showToast('❌ Data e hora são obrigatórias', 'error');
        return false;
    }
    
    // Validar se data/hora não é no passado (usando timezone local)
    try {
        const selectedDateTime = new Date(`${dateInput.value}T${timeInput.value}:00`);
        const now = new Date();
        
        if (selectedDateTime <= now) {
            event.preventDefault();
            showToast('❌ A data e hora devem ser no futuro', 'error');
            return false;
        }
    } catch (error) {
        console.warn('Erro na validação de data/hora:', error);
        // Permitir continuar se houver erro na validação
    }
    
    return true;
}

function updateLembreteTimers() {
    // Atualizar todos os timers de lembretes na página
    const lembreteCards = document.querySelectorAll('.lembrete-card');
    
    lembreteCards.forEach((card, index) => {
        const timeElement = card.querySelector('.time-remaining span');
        if (timeElement) {
            // Aqui você poderia recalcular o tempo restante
            // Por simplicidade, vamos apenas atualizar classes visuais
            updateLembreteVisualState(card);
        }
    });
}

function updateLembreteVisualState(card) {
    const timeRemaining = card.querySelector('.time-remaining');
    const timeText = timeRemaining.querySelector('span').textContent;
    
    // Remover classes antigas
    timeRemaining.classList.remove('due-soon', 'expired');
    card.classList.remove('due-soon', 'expired');
    
    // Adicionar classes baseadas no texto
    if (timeText.includes('Vencido')) {
        timeRemaining.classList.add('expired');
        card.classList.add('expired');
    } else if (timeText.includes('minuto') || timeText.includes('hora')) {
        // Se for menos de algumas horas, considerar "due soon"
        const isMinutes = timeText.includes('minuto');
        const isHours = timeText.includes('hora');
        
        if (isMinutes || (isHours && parseInt(timeText) <= 2)) {
            timeRemaining.classList.add('due-soon');
            card.classList.add('due-soon');
        }
    }
}

function showToast(message, type = 'info') {
    // Criar toast notification
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <span>${message}</span>
            <button class="toast-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Adicionar estilos inline se não existirem
    if (!document.querySelector('#toast-styles')) {
        const styles = document.createElement('style');
        styles.id = 'toast-styles';
        styles.textContent = `
            .toast {
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--bg-card);
                color: var(--text-primary);
                padding: 12px 16px;
                border-radius: var(--border-radius-sm);
                box-shadow: var(--shadow-lg);
                z-index: 10002;
                transform: translateX(100%);
                transition: transform 0.3s ease;
                max-width: 300px;
            }
            .toast.show { transform: translateX(0); }
            .toast-info { border-left: 4px solid var(--info); }
            .toast-warning { border-left: 4px solid var(--warning); }
            .toast-error { border-left: 4px solid var(--error); }
            .toast-content {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 12px;
            }
            .toast-close {
                background: none;
                border: none;
                color: var(--text-muted);
                cursor: pointer;
                padding: 4px;
            }
            .toast-close:hover { color: var(--text-primary); }
        `;
        document.head.appendChild(styles);
    }
    
    document.body.appendChild(toast);
    
    // Mostrar toast
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Remover automaticamente
    setTimeout(() => {
        if (toast.parentElement) {
            toast.classList.remove('show');
            setTimeout(() => {
                if (toast.parentElement) {
                    document.body.removeChild(toast);
                }
            }, 300);
        }
    }, 4000);
}

// Função global para configurar lembretes rápidos
function setQuickReminder(hours) {
    const dateInput = document.querySelector('input[name="prazo_date"]');
    const timeInput = document.querySelector('input[name="prazo_time"]');
    
    if (dateInput && timeInput) {
        // Usar timezone local para cálculos
        const futureDate = new Date();
        futureDate.setHours(futureDate.getHours() + hours);
        
        // Formatar para inputs HTML
        const year = futureDate.getFullYear();
        const month = String(futureDate.getMonth() + 1).padStart(2, '0');
        const day = String(futureDate.getDate()).padStart(2, '0');
        const hour = String(futureDate.getHours()).padStart(2, '0');
        const minute = String(futureDate.getMinutes()).padStart(2, '0');
        
        dateInput.value = `${year}-${month}-${day}`;
        timeInput.value = `${hour}:${minute}`;
        
        const hoursText = hours !== 1 ? 's' : '';
        showToast(`⏰ Lembrete configurado para ${hours} hora${hoursText} a partir de agora`, 'info');
    }
}

// Função para debug de timezone
function showTimezoneDebug() {
    fetch('/timezone-info')
        .then(response => response.json())
        .then(data => {
            console.log('🌍 Informações de Timezone:', data);
            
            const clientInfo = JSON.parse(localStorage.getItem('clientTimezone') || '{}');
            console.log('💻 Timezone do Cliente:', clientInfo);
            
            showToast(`Timezone: ${data.timezone_info.timezone}`, 'info');
        })
        .catch(error => {
            console.error('Erro ao obter info de timezone:', error);
        });
}
