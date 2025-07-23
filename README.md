# StuddyGenda - Sua Agenda Inteligente 📚✨

Projeto da disciplina **Orientação a Objetos (2025.1)** demonstrando os principais pilares da Programação Orientada a Objetos (POO) através de um sistema web elegante e funcional.

### ✨ Principais Funções Implementadas

- **🔄 Interface por Tabs**: Navegação intuitiva e organizada
- **🌙 Modo Escuro/Claro**: Alternância suave entre temas
- **📱 Design Responsivo**: Otimizado para todas as telas
- **♿ Acessibilidade**: Suporte a navegação por teclado e leitores de tela
- **⚡ Performance**: Carregamento otimizado e animações fluidas
- **🔃 Sincronização em tempo real** entre múltiplos dispositivos

### 🎭 Sistema de Temas
- **Modo Escuro**: Design elegante com gradientes e glass morphism
- **Modo Claro**: Interface limpa e profissional
- **Persistência**: Preferência de tema salva automaticamente

### 📊 Funcionalidades por Tab

#### 📝 **Tab Lembretes**
- ➕ Formulário intuitivo para novos lembretes
- 🏷️ Campos: Título, Descrição, Prazo
- 📅 Exibição organizada com destaque temporal
- 🎨 Cards visuais com bordas coloridas

#### ✅ **Tab Tarefas**
- 🎯 Sistema de prioridades (Alta/Média/Baixa)
- 🔴 Indicadores visuais por prioridade
- 📊 Organização clara e funcional
- ⭐ Seletor dropdown amigável

#### ⏱️ **Tab Timers**
- ⏰ Presets rápidos (Pomodoro, Pausa, Hora)
- ▶️ Controles de play/pause integrados
- 🔔 Notificações de conclusão
- 📱 Interface tipo cronômetro

## 🛠️ **Tecnologias e Arquitetura**

### Backend (Python)
- **Framework**: Bottle.py
- **Padrão**: MVC (Model-View-Controller)
- **Persistência**: JSON
- **POO**: Classes e herança implementadas

### Websocket
- **Servidor WebSocket**: Usando `gevent` e `gevent-websocket`
- **Gerenciador de Conexões**: `websocketManager.py` controla todas as conexões
- **Cliente JavaScript**: `websocket.js` gerencia conexões do lado do cliente

### Frontend
- **HTML5**: Estrutura semântica moderna
- **CSS3**: Variáveis CSS, Grid, Flexbox, Animações
- **JavaScript ES6+**: Modular e orientado a eventos
- **Ícones**: Font Awesome 6.4.0

## 📝 Definição do Problema

A organização e o planejamento das atividades acadêmicas são desafios comuns para estudantes universitários. A falta de um sistema centralizado e **visualmente agradável** dificulta o acompanhamento de tarefas, prazos e compromissos.

## 💡 Solução Proposta

O **StuddyGenda** é um aplicativo web **moderno e intuitivo** que combina funcionalidade com design excepcional. Com navegação por tabs e interface responsiva, oferece uma experiência superior para gerenciamento acadêmico.

## 🚀 Pré-requisitos e Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/cunha-luiss/StuddyGenda-POO.git
cd StuddyGenda-POO
```

### 2. Instale o Python (>= 3.8)
Certifique-se de ter o Python instalado. [Download Python](https://www.python.org/downloads/)

### 3. Instale as dependências do projeto
```bash
pip install -r requirements.txt
```

### 4. Execute o servidor Bottle
```bash
python runHere.py
```
O servidor estará disponível, normalmente, em [http://localhost:8080](http://localhost:8080).

## 🖥️ Uso/Casos de Uso

A SER IMPLEMENTADO...

## ⌨️ **Atalhos de Teclado**

- **Ctrl/Cmd + 1, 2, 3**: Alternar entre tabs
- **Ctrl/Cmd + D**: Alternar tema escuro/claro
- **Esc**: Fechar modais
- **Tab**: Navegação acessível

## 🛜 Status de Conexão Webscoket
No cabeçalho da aplicação:
- 🟢 **Sincronizado** - Conexão ativa
- 🔴 **Desconectado** - Sem conexão (tentando reconectar)
- ⚠️ **Erro de conexão** - Problema na conexão

## 🔮 **Próximas Funcionalidades**

- 📊 **Dashboard**: Estatísticas de produtividade
- 🔔 **Notificações**: Lembretes push

## 🔎 Observações

- O projeto tem fins didáticos e visa ilustrar conceitos de POO em Python e práticas de desenvolvimento web.
- Pode ser necessário ajustar configurações de porta/firewall dependendo do seu ambiente.
- Caso deseje contribuir, sinta-se à vontade para abrir issues ou pull requests!
- Para dúvidas ou sugestões, utilize a aba de Issues do repositório.

---

Desenvolvido para a disciplina de **Orientação a Objetos** – 2025.1
