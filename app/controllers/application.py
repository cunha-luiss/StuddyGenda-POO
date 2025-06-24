from app.controllers.dataRecord import DataRecord
from bottle import template, redirect, request
from app.controllers.lembreteRecord import LembreteRecord


class Application():

    def __init__(self):

        self.pages = {
            'login': self.login,
            'signup': self.signup,
            'appGenda': self.appGenda
        }

        self.__model= DataRecord()
        self.__current_email = None

    def signup(self):
        return template('app/views/html/signup')

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
        lembretes = lembrete_record.read()
        return template('app/views/html/appGenda', lembretes=lembretes)
        
    def new_user(self):
        return self.__model

    def render(self,page,parameter=None):
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content()
        else:
            return content(parameter)

    def get_session_id(self):
        return request.get_cookie('session_id')


    def helper(self):
        return template('app/views/html/helper')


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
        titulo = request.forms.get('titulo')
        desc = request.forms.get('desc')
        prazo = request.forms.get('prazo')
        lembrete_record.book(titulo, desc, prazo)
        return redirect('/appGenda')

    def delete_lembrete(self, index):
        session_id = self.get_session_id()
        if not session_id:
            return redirect('/login')
        user_email = self.__model.getemail(session_id)
        lembrete_record = LembreteRecord(user_email)
        lembrete_record.delete(int(index))
        return redirect('/appGenda')