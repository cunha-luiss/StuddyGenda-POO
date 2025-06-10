from app.models.user_account import UserAccount
import json
import os
import uuid


class DataRecord():
    """Banco de dados JSON para o recurso Usuários"""

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self._path = os.path.join(base_dir, 'db', 'user_accounts.json')
        if not os.path.exists(self._path):
            with open(self._path, 'w', encoding='utf-8') as f:
                json.dump([], f)

        self.__user_accounts= []
        self.__authenticated_users = {}
        self.read()


    def read(self):
        try:
            with open(self._path, "r", encoding='utf-8') as arquivo_json:
                user_data = json.load(arquivo_json)
                self.__user_accounts = [UserAccount(**data) for data in user_data]
        except FileNotFoundError:
            self.__user_accounts.append(UserAccount('Guest', '010101'))


    def book(self,email,password):
        new_user= UserAccount(email,password)
        self.__user_accounts.append(new_user)
        with open(self._path, "w", encoding='utf-8') as arquivo_json:
            user_data = [vars(user_account) for user_account in \
            self.__user_accounts]
            json.dump(user_data, arquivo_json)


    def getCurrentUser(self,session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id]
        else:
            return None


    def getemail(self,session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id].email
        else:
            return None


    def getUserSessionId(self, email):
        for session_id in self.__authenticated_users:
            if email == self.__authenticated_users[session_id].email:
                return session_id
        return None  # Retorna None se o usuário não for encontrado


    def checkUser(self, email, password):
        for user in self.__user_accounts:
            if user.email == email and user.password == password:
                session_id = str(uuid.uuid4())  # Gera um ID de sessão único
                self.__authenticated_users[session_id] = user
                return session_id  # Retorna o ID de sessão para o usuário
        return None


    def logout(self, session_id):
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id] # Remove o usuário logado