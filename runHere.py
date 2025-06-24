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

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')


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
    new_userT = ctl.new_user()
    new_userT.book(email, password)
    session_id, email= ctl.authenticate_user(email, password)

    if session_id:
        response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
        redirect(f'/appGenda')
    else:
        return redirect('/signup')

@app.route('/appGenda', method='GET')
def appGenda_page():
    return ctl.render('appGenda')

@app.route('/add_lembrete', method='POST')
def add_lembrete_route():
    return ctl.add_lembrete()

@app.route('/delete_lembrete/<index>', method='GET')
def delete_lembrete_route(index):
    return ctl.delete_lembrete(index)

@app.route('/logout', method='POST')
def logout():
    ctl.logout_user()
    response.delete_cookie('session_id')
    redirect('/')
#-----------------------------------------------------------------------------


if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)
