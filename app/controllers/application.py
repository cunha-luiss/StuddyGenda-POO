from app.controllers.dataRecord import DataRecord
from app.controllers.websocketManager import websocket_manager
from app.controllers.timezoneHelper import timezone_helper
from bottle import template, redirect, request
from app.controllers.lembreteRecord import LembreteRecord
from app.controllers.taskRecord import TaskRecord
from app.controllers.timerRecord import TimerRecord

def decode_form_data(data):
    """Decodifica dados de formulário que chegam com encoding incorreto"""
    if data is None:
        return ''
    try:
        # Tenta decodificar se veio como latin1 mas é UTF-8
        return data.encode('latin1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        # Se falhar, retorna o dado original
        return data

class Application():

    def __init__(self):

        self.pages = {
            'login': self.login,
            'signup': self.signup,
            'appGenda': self.appGenda,
        }

        self.__model= DataRecord()
        self.__current_email = None

    def signup(self, error=None):
        return template('app/views/html/signup', error=error)

    def login(self,email=None):
        if self.is_authenticated(email):
            session_id = self.get_session_id()
            user = self.__model.getCurrentUser(session_id)
            return template('app/views/html/login', current_user=user)
        else:
            return template('app/views/html/login', current_user=None)
    
    def appGenda(self):
        session_id = self.get_session_id()
        if not session_id:
            return redirect('/login')
        user_email = self.__model.getemail(session_id)
        lembrete_record = LembreteRecord(user_email)
        task_record = TaskRecord(user_email)
        timer_record = TimerRecord(user_email)
        lembretes = lembrete_record.read()
        tasks = task_record.read()
        timers = timer_record.read()
        return template('app/views/html/appGenda', lembretes=lembretes, tasks=tasks, timers=timers)
        
    def new_user(self):
        return self.__model

    def render(self,page,parameter=None):
        content = self.pages.get(page, self.login)
        if not parameter:
            return content()
        else:
            return content(parameter)

    def get_session_id(self):
        return request.get_cookie('session_id')


    def is_authenticated(self, email):
        session_id = self.get_session_id()
        current_email = self.__model.getemail(session_id)
        return email == current_email


    def authenticate_user(self, email, password):
        session_id = self.__model.checkUser(email, password)
        if session_id:
            self.logout_user()
            self.__current_email = self.__model.getemail(session_id)
            return session_id, email
        return None, None


    def logout_user(self):
        self.__current_email= None
        session_id = self.get_session_id()
        if session_id:
            self.__model.logout(session_id)

    def add_lembrete(self):
        session_id = self.get_session_id()
        if not session_id:
            return redirect('/login')
        user_email = self.__model.getemail(session_id)
        lembrete_record = LembreteRecord(user_email)
        
        # Capturar dados com encoding correto
        titulo = decode_form_data(request.forms.get('titulo'))
        desc = decode_form_data(request.forms.get('desc'))
        date_str = request.forms.get('prazo_date')  # Nova: data
        time_str = request.forms.get('prazo_time')  # Nova: hora
        
        # Criar datetime local e converter para UTC para armazenamento
        try:
            local_datetime = timezone_helper.create_local_datetime(date_str, time_str)
            prazo_utc = timezone_helper.to_utc_isoformat(local_datetime)
            prazo_formatted = timezone_helper.to_local_string(local_datetime)
        except Exception as e:
            print(f"❌ Erro ao processar data/hora: {e}")
            # Fallback para formato antigo
            from datetime import datetime
            prazo_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            prazo_utc = prazo_datetime.isoformat()
            prazo_formatted = prazo_datetime.strftime('%d/%m/%Y às %H:%M')
        
        lembrete_record.book(titulo, desc, prazo_utc)
        
        # Sincronizar via WebSocket
        lembrete_data = {
            'titulo': titulo,
            'desc': desc,
            'prazo': prazo_utc,
            'prazo_formatted': prazo_formatted,
            'timezone_info': timezone_helper.get_timezone_info()
        }
        websocket_manager.sync_lembrete_added(user_email, lembrete_data)
        
        return redirect('/appGenda')

    def delete_lembrete(self, index):
        session_id = self.get_session_id()
        if not session_id:
            return redirect('/login')
        user_email = self.__model.getemail(session_id)
        lembrete_record = LembreteRecord(user_email)
        lembrete_record.delete(int(index))
        
        # Sincronizar via WebSocket
        websocket_manager.sync_lembrete_deleted(user_email, int(index))
        
        return redirect('/appGenda')

    def add_task(self):
        session_id = self.get_session_id()
        if not session_id:
            return redirect('/login')
        user_email = self.__model.getemail(session_id)
        task_record = TaskRecord(user_email)
        
        # Capturar dados com encoding correto
        nome = decode_form_data(request.forms.get('nome'))
        prioridade = request.forms.get('prioridade')
        
        # Converter prioridade para inteiro
        try:
            prioridade = int(prioridade)
        except (ValueError, TypeError):
            prioridade = 3
            
        task_record.book(nome, prioridade)
        
        # Sincronizar via WebSocket
        task_data = {
            'nome': nome,
            'prioridade': prioridade
        }
        websocket_manager.sync_task_added(user_email, task_data)
        
        return redirect('/appGenda')

    def delete_task(self, index):
        session_id = self.get_session_id()
        if not session_id:
            return redirect('/login')
        user_email = self.__model.getemail(session_id)
        task_record = TaskRecord(user_email)
        task_record.delete(int(index))
        
        # Sincronizar via WebSocket
        websocket_manager.sync_task_deleted(user_email, int(index))
        
        return redirect('/appGenda')

    def add_timer(self):
        session_id = self.get_session_id()
        if not session_id:
            return redirect('/login')
        user_email = self.__model.getemail(session_id)
        timer_record = TimerRecord(user_email)
        tempo = request.forms.get('tempo')
        timer_record.book(tempo)
        
        # Sincronizar via WebSocket
        timer_data = {
            'tempo': tempo
        }
        websocket_manager.sync_timer_added(user_email, timer_data)
        
        return redirect('/appGenda')

    def delete_timer(self, index):
        session_id = self.get_session_id()
        if not session_id:
            return redirect('/login')
        user_email = self.__model.getemail(session_id)
        timer_record = TimerRecord(user_email)
        timer_record.delete(int(index))
        
        # Sincronizar via WebSocket
        websocket_manager.sync_timer_deleted(user_email, int(index))
        
        return redirect('/appGenda')