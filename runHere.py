from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response
import sys
import os
import bottle

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

# Configuração UTF-8 para o sistema
if sys.platform.startswith('win'):
    # Para Windows, garante que o console suporte UTF-8
    os.system('chcp 65001 > nul 2>&1')

app = Bottle()
ctl = Application()

# Configurar encoding padrão para templates
bottle.BaseTemplate.settings = {'autoescape': True}

# Configurar Bottle para UTF-8
app.config['bottle.request.decode_errors'] = 'replace'
app.config['bottle.request.encoding'] = 'utf-8'

# Garantir que todas as respostas tenham charset UTF-8
@app.hook('after_request')
def enable_cors():
    if not response.content_type.startswith('text/'):
        return
    if 'charset' not in response.content_type:
        response.content_type += '; charset=UTF-8'

# Configurar request para UTF-8
@app.hook('before_request')
def before_request():
    # Garantir que o request seja decodificado corretamente
    if hasattr(request, 'forms'):
        request.environ.setdefault('CONTENT_TYPE', 'application/x-www-form-urlencoded; charset=utf-8')


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

#-----------------------------------------------------------------------------
# Suas rotas aqui:
@app.route('/')
@app.route('/login', method='GET')
def action_login():
    return ctl.render('login')

@app.route('/logi', method='POST')
def action_portal():
    # Capturar dados com encoding correto
    email = decode_form_data(request.forms.get('email'))
    password = decode_form_data(request.forms.get('password'))
    
    session_id, email= ctl.authenticate_user(email, password)
    if session_id:
        response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
        return redirect('/appGenda')
    else:
        return redirect('/login')
    
@app.route('/signup', method='GET')
def action_signup():
    return ctl.render('signup')

@app.route('/signu', method='POST')
def action_signup_post():
    # Capturar dados com encoding correto
    email = decode_form_data(request.forms.get('email'))
    password = decode_form_data(request.forms.get('password'))
    
    model = ctl.new_user()

    # Se já existir conta com o email
    if model.exists(email):
        return template('app/views/html/signup', error='Já existe uma conta com este email')
    # Se senha menor que 8 caracteres
    elif len(password) < 8:
        return template('app/views/html/signup', error='Senha deve ter ao menos 8 caracteres')

    model.book(email, password)
    session_id, _ = ctl.authenticate_user(email, password)
    response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
    return redirect('/appGenda')

@app.route('/appGenda', method='GET')
def appGenda_page():
    return ctl.render('appGenda')

@app.route('/add_lembrete', method='POST')
def add_lembrete_route():
    return ctl.add_lembrete()

@app.route('/delete_lembrete/<index>', method='GET')
def delete_lembrete_route(index):
    return ctl.delete_lembrete(index)

@app.route('/add_task', method='POST')
def add_task_route():
    return ctl.add_task()

@app.route('/delete_task/<index>', method='GET')
def delete_task_route(index):
    return ctl.delete_task(index)

@app.route('/add_timer', method='POST')
def add_timer_route():
    return ctl.add_timer()

@app.route('/delete_timer/<index>', method='GET')
def delete_timer_route(index):
    return ctl.delete_timer(index)

@app.route('/logout', method='POST')
def logout():
    ctl.logout_user()
    response.delete_cookie('session_id')
    return redirect('/')
#-----------------------------------------------------------------------------


if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)
