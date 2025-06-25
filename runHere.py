from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response

app = Bottle()
ctl = Application()


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
    email = request.forms.get('email')
    password = request.forms.get('password')
    session_id, email= ctl.authenticate_user(email, password)
    if session_id:
        response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
        redirect(f'/appGenda')
    else:
        return redirect('/login')
    
@app.route('/signup', method='GET')
def action_signup():
    return ctl.render('signup')

@app.route('/signu', method='POST')
def action_portal():
    email = request.forms.get('email')
    password = request.forms.get('password')
    model = ctl.new_user()

    # Se já existir conta com o email
    if model.exists(email):
        return template('app/views/html/signup', error='Já existe uma conta com este email')
    # Se senha menor que 8 caracteres
    elif len(password) < 8:
        return template('app/views/html/signup', error='Senha deve ter ao menos 8 caracteres')

    # Cria usuário e autentica
    model.book(email, password)
    session_id, _ = ctl.authenticate_user(email, password)
    response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
    redirect(f'/appGenda')

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
    redirect('/')
#-----------------------------------------------------------------------------


if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)
