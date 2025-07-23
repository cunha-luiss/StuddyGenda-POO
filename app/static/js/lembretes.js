/**
 * Script para funcionalidades específicas de lembretes
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeLembreteFeatures();
    updateLembreteTimers();
    
    // Atualizar timers a cada minuto
    setInterval(updateLembreteTimers, 60000);
});

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
        const now = new Date();
        const tomorrow = new Date(now);
        tomorrow.setDate(tomorrow.getDate() + 1);
        
        // Definir data padrão como amanhã
        dateInput.value = tomorrow.toISOString().split('T')[0];
        
        // Definir hora padrão como 9:00
        timeInput.value = '09:00';
        
        // Validar que a data não seja no passado
        dateInput.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            if (selectedDate < today) {
                this.value = today.toISOString().split('T')[0];
                showToast('⚠️ A data não pode ser no passado', 'warning');
            }
        });
        
        // Validar hora se for hoje
        timeInput.addEventListener('change', function() {
            const selectedDate = new Date(dateInput.value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            if (selectedDate.getTime() === today.getTime()) {
                const [hours, minutes] = this.value.split(':');
                const selectedTime = new Date();
                selectedTime.setHours(parseInt(hours), parseInt(minutes), 0, 0);
                
                if (selectedTime <= new Date()) {
                    const futureTime = new Date();
                    futureTime.setHours(futureTime.getHours() + 1);
                    this.value = futureTime.toTimeString().slice(0, 5);
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
    
    // Validar se data/hora não é no passado
    const selectedDateTime = new Date(`${dateInput.value}T${timeInput.value}`);
    if (selectedDateTime <= new Date()) {
        event.preventDefault();
        showToast('❌ A data e hora devem ser no futuro', 'error');
        return false;
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
        const futureDate = new Date();
        futureDate.setHours(futureDate.getHours() + hours);
        
        dateInput.value = futureDate.toISOString().split('T')[0];
        timeInput.value = futureDate.toTimeString().slice(0, 5);
        
        showToast(`⏰ Lembrete configurado para ${hours} hora${hours !== 1 ? 's' : ''} a partir de agora`, 'info');
    }
}
