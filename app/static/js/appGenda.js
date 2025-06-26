// ===== CONTROLE DE TABS =====
document.addEventListener('DOMContentLoaded', function() {
    initializeTabs();
    initializeThemeToggle();
    initializeModals();
    initializeTimerPresets();
    initializeRobot(); // ✨ Novo: inicializar robô
});

function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Remove active class from all tabs and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
            
            // Animate tab transition
            const activeContent = document.getElementById(targetTab);
            activeContent.style.opacity = '0';
            activeContent.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                activeContent.style.opacity = '1';
                activeContent.style.transform = 'translateY(0)';
            }, 50);
        });
    });
}

// ===== CONTROLE DE TEMA =====
function initializeThemeToggle() {
    const themeToggle = document.getElementById('toggleTheme');
    const themeIcon = document.getElementById('themeIcon');
    const html = document.documentElement;
    
    // Check for saved theme preference or default to dark mode
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        html.classList.toggle('light-mode', savedTheme === 'light');
        updateThemeIcon(savedTheme === 'light');
    }
    
    themeToggle.addEventListener('click', () => {
        const isLightMode = html.classList.toggle('light-mode');
        localStorage.setItem('theme', isLightMode ? 'light' : 'dark');
        updateThemeIcon(isLightMode);
        
        // Add animation to theme toggle
        themeToggle.style.transform = 'scale(0.9) rotate(180deg)';
        setTimeout(() => {
            themeToggle.style.transform = 'scale(1) rotate(0deg)';
        }, 200);
    });
}

function updateThemeIcon(isLightMode) {
    const themeIcon = document.getElementById('themeIcon');
    themeIcon.className = isLightMode ? 'fas fa-sun' : 'fas fa-moon';
    
    // Mantém consistência com login/signup
    if (isLightMode) {
        themeIcon.style.color = '#f39c12'; // Sol dourado
    } else {
        themeIcon.style.color = '#f1c40f'; // Lua amarela
    }
}

// ===== MODAIS =====
let deleteUrl = null;

function initializeModals() {
    const modal = document.getElementById('confirmModal');
    
    // Close modal when clicking outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            closeModal();
        }
    });
}

function confirmDelete(url, itemType) {
    deleteUrl = url;
    const modal = document.getElementById('confirmModal');
    const modalText = modal.querySelector('p');
    
    modalText.textContent = `Tem certeza que deseja excluir este ${itemType}?`;
    modal.classList.add('show');
    
    // Add animation
    const modalContent = modal.querySelector('.modal-content');
    modalContent.style.transform = 'scale(0.8)';
    modalContent.style.opacity = '0';
    
    setTimeout(() => {
        modalContent.style.transform = 'scale(1)';
        modalContent.style.opacity = '1';
    }, 50);
}

function closeModal() {
    const modal = document.getElementById('confirmModal');
    const modalContent = modal.querySelector('.modal-content');
    
    modalContent.style.transform = 'scale(0.8)';
    modalContent.style.opacity = '0';
    
    setTimeout(() => {
        modal.classList.remove('show');
        deleteUrl = null;
    }, 200);
}

function executeDelete() {
    if (deleteUrl) {
        window.location.href = deleteUrl;
    }
}

// ===== TIMER FUNCTIONALITY =====
let activeTimers = new Map();

function initializeTimerPresets() {
    // Timer presets are already handled by onclick attributes in HTML
}

function setTime(minutes) {
    const timeInput = document.querySelector('input[name="tempo"]');
    if (timeInput) {
        timeInput.value = minutes;
        
        // Add visual feedback
        timeInput.style.borderColor = 'var(--primary-color)';
        timeInput.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)';
        
        setTimeout(() => {
            timeInput.style.borderColor = '';
            timeInput.style.boxShadow = '';
        }, 1000);
    }
}

function startTimer(timerId, minutes) {
    const button = event.target.closest('button');
    const card = button.closest('.timer-card');
    const timeDisplay = card.querySelector('.timer-time');
    const unitDisplay = card.querySelector('.timer-unit');
    
    if (activeTimers.has(timerId)) {
        // Stop timer
        clearInterval(activeTimers.get(timerId));
        activeTimers.delete(timerId);
        button.innerHTML = '<i class="fas fa-play"></i> Iniciar';
        button.classList.remove('btn-danger');
        button.classList.add('btn-secondary');
        timeDisplay.textContent = minutes;
        unitDisplay.textContent = 'minutos';
        return;
    }
    
    // Start timer
    let totalSeconds = minutes * 60;
    button.innerHTML = '<i class="fas fa-stop"></i> Parar';
    button.classList.remove('btn-secondary');
    button.classList.add('btn-danger');
    
    const interval = setInterval(() => {
        const mins = Math.floor(totalSeconds / 60);
        const secs = totalSeconds % 60;
        
        timeDisplay.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        unitDisplay.textContent = 'restante';
        
        if (totalSeconds <= 0) {
            clearInterval(interval);
            activeTimers.delete(timerId);
            
            // Timer finished
            timeDisplay.textContent = '00:00';
            unitDisplay.textContent = 'finalizado!';
            button.innerHTML = '<i class="fas fa-redo"></i> Reiniciar';
            button.classList.remove('btn-danger');
            button.classList.add('btn-secondary');
            
            // Show notification
            showNotification('Timer finalizado!', 'success');
            
            // Play sound (if available)
            try {
                const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DvuW8gCDJ+z/DWfS0IIWq+8+SAOA4PVafg8M5jHAU4k9n0w3ojBSl+zPLaizsIGGS57OGYTQwOT6Lf8Lh4HQU2jdPzx3giBSF1xe/bkUELElyx6O2nVBUI');
                audio.play();
            } catch (e) {
                console.log('Audio notification not available');
            }
            
            return;
        }
        
        totalSeconds--;
    }, 1000);
    
    activeTimers.set(timerId, interval);
}

// ===== NOTIFICATIONS =====
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--bg-card);
        color: var(--text-primary);
        padding: 1rem;
        border-radius: var(--border-radius);
        border-left: 4px solid ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#4CAF50'};
        box-shadow: var(--shadow-lg);
        z-index: 1001;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// ===== FORM ENHANCEMENTS =====
document.addEventListener('DOMContentLoaded', function() {
    // Add loading states to forms
    const forms = document.querySelectorAll('.add-form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adicionando...';
            submitButton.disabled = true;
            
            // Re-enable after a delay (in case of error)
            setTimeout(() => {
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }, 5000);
        });
    });
    
    // Add input validation feedback
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.style.borderColor = 'var(--error)';
                this.style.boxShadow = '0 0 0 3px rgba(255, 107, 107, 0.1)';
            } else {
                this.style.borderColor = '';
                this.style.boxShadow = '';
            }
        });
        
        input.addEventListener('input', function() {
            if (this.style.borderColor === 'var(--error)' && this.value.trim()) {
                this.style.borderColor = 'var(--success)';
                this.style.boxShadow = '0 0 0 3px rgba(0, 212, 170, 0.1)';
                
                setTimeout(() => {
                    this.style.borderColor = '';
                    this.style.boxShadow = '';
                }, 2000);
            }
        });
    });
});

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + 1, 2, 3 to switch tabs
    if ((e.ctrlKey || e.metaKey) && e.key >= '1' && e.key <= '3') {
        e.preventDefault();
        const tabIndex = parseInt(e.key) - 1;
        const tabButtons = document.querySelectorAll('.tab-btn');
        if (tabButtons[tabIndex]) {
            tabButtons[tabIndex].click();
        }
    }
    
    // Ctrl/Cmd + D to toggle theme
    if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
        e.preventDefault();
        document.getElementById('toggleTheme').click();
    }
});

// ===== SMOOTH SCROLLING =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===== ACCESSIBILITY IMPROVEMENTS =====
document.addEventListener('DOMContentLoaded', function() {
    // Add ARIA labels and roles where needed
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach((button, index) => {
        button.setAttribute('role', 'tab');
        button.setAttribute('aria-selected', button.classList.contains('active'));
        button.setAttribute('tabindex', button.classList.contains('active') ? '0' : '-1');
    });
    
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.setAttribute('role', 'tabpanel');
        content.setAttribute('aria-hidden', !content.classList.contains('active'));
    });
});

// ===== ERROR HANDLING =====
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    showNotification('Ocorreu um erro inesperado. Tente recarregar a página.', 'error');
});

// ===== OFFLINE DETECTION =====
window.addEventListener('online', () => {
    showNotification('Conexão restaurada!', 'success');
});

window.addEventListener('offline', () => {
    showNotification('Você está offline. Algumas funcionalidades podem não funcionar.', 'warning');
});

// ===== ANIMAÇÃO DO ROBÔ =====
function initializeRobot() {
    const eyes = document.querySelectorAll('.eye');
    
    // Piscar aleatório dos olhos
    function randomBlink() {
        const randomEye = eyes[Math.floor(Math.random() * eyes.length)];
        randomEye.classList.add('active');
        
        setTimeout(() => {
            randomEye.classList.remove('active');
        }, 500);
        
        // Próximo piscar em intervalo aleatório (2-6 segundos)
        setTimeout(randomBlink, Math.random() * 4000 + 2000);
    }
    
    // Iniciar após um delay
    if (eyes.length > 0) {
        setTimeout(randomBlink, 2000);
    }
    
    // Interação com hover - ambos os olhos piscam
    const robotContainer = document.querySelector('.robot-container');
    if (robotContainer) {
        robotContainer.addEventListener('mouseenter', () => {
            eyes.forEach(eye => eye.classList.add('active'));
        });
        
        robotContainer.addEventListener('mouseleave', () => {
            eyes.forEach(eye => eye.classList.remove('active'));
        });
    }
}