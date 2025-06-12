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
        response.set_cookie('session_id', session_id, httponly=True, \
        secure=True, max_age=3600)
        redirect(f'/login/{email}')
    else:
        return redirect('/login')
    
@app.route('/signup', method='GET')
def action_signup():
    return ctl.render('signup')
#-----------------------------------------------------------------------------


if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)
