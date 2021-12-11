from flask import Flask, request
import json

from middleware.auth import AuthorizationMiddleware
app= Flask(__name__)
app.wsgi_app= AuthorizationMiddleware(app.wsgi_app)

# вс джиай обртка для питона, чтобы общаться с серверами
user = {
    '1' : {'name': 'admin','money': 100500},
    '2' : {'name': 'ivan','money': 200500}
}

@app.route('/')
def index():
    print('I am from app')
    return ""

@app.route('/get-money')
def get_money_handler():
    user_id = request.headers.get('Auth-Middleware')
    return json.dumps({'user_id': user_id, 'money': user.get(user_id)['money']})

if __name__=='__main__':
    app.run(host='127.0.0.1', port=5001)