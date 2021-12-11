from werkzeug.wrappers import Request, Response
from .base import Middleware
import  jwt

class AuthorizationMiddleware(Middleware):
    def __init__(self, wsgi_app):
        self.wsgi_app=wsgi_app

    def _generate_token(self,request):
        try:
            body = request.json
            if not isinstance(body,dict):
                raise TypeError('Invalid body')
            username = body.get('username','')
            password = body.get('password','')

            if username == 'admin' and password == 'admin':
                user_id='1'
                return jwt.encode(
                    payload={
                    'username':username,
                    'password': password,
                    'user_id':user_id
                },
                key='my super key',
                algorithm='HS256'
                )
            return None
        except TypeError:
            return None

    def _decode_token(self,request):
        try:
            token = request.headers.get('Authorization', '')
            decode = jwt.decode(token, key='my super key', algorithms='HS256')['user_id']
            return decode
        except (KeyError, jwt.exceptions.DecodeError):
            return None

    def __call__(self, environ, start_response):
        request=Request(environ) # перегрузили request
        if request.path == '/token' and request.method == 'POST':
            token = self._generate_token(request)
            if token is None:
                return Response('No such user or invalid request body', status=400)(environ,start_response)
                # проинициализировали и сразу вызвали объект, сделали так, чтобы не вводить новую переменную
            return Response(token, status=200)(environ,start_response)
        else:
            user_id = self._decode_token(request)
            if user_id:
                environ['HTTP_AUTH_MIDDLEWARE'] = user_id
                return self.wsgi_app(environ,start_response)
            return Response('Unauthorized', status=403)(environ, start_response)
