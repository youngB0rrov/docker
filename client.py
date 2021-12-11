# Собственный мидлвеер
# это можно представить как аналог декоратора,
# но декораторы работают на уровне функций или уровне классов, а это как декоратор всей информационной системы
# будем работать с json
import json
import requests
def get_token(username,password):
    headers = {'Content-Type' : 'application/json'}
    data = json.dumps({'username' : username, 'password' : password})
    response = requests.post('http://127.0.0.1:5001/token', data=data, headers=headers)
    return response.text

def make_get_request(token):
    headers = {'Authorization': token}
    response = requests.get('http://127.0.0.1:5001/get-money', headers=headers) #get-money проверяет через айпи на сервере
    return response.text


if __name__ == '__main__':
    token = get_token(username='admin', password='admin')
    print('token', token)
    result = make_get_request(token=token)
    print('result', result)