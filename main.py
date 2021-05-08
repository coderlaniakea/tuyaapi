import hmac
from hashlib import sha256


def get_sign(key, msg):
    key = key.encode('utf-8')
    msg = msg.encode('utf-8')
    return hmac.new(key, msg, digestmod=sha256).hexdigest().upper()





def get_token(access_id, secret, t):
    """
        token接口：sign = HMAC-SHA256(client_id + t, secret).toUpperCase() 
        非token接口：sign = HMAC-SHA256(client_id + access_token + t, secret).toUpperCase()
    """
 
    link_str = access_id + t

    sign = get_sign(secret, link_str)

    endpoint = r'https://openapi.tuyaus.com'
    headers = {
        'client_id': access_id,
        'sign': sign,
        'sign_method': 'HMAC-SHA256',
        't': t,
        # 'access_token': '', # 获取和刷新token不需要
        # 'Content-Type': 'application/json'
    }
    

    url = '{}/v1.0/token?grant_type=1'.format(endpoint)
    resp = requests.get(url, headers=headers)
    print('GET resp: ' + resp.text)
    response = json.loads(resp.text)

    result = response['result']
    access_token = result['access_token']
    refresh_token = result['refresh_token']

    print('access_token：', access_token)
    print('refresh_token：', refresh_token)
    return access_token




if __name__ == '__main__':

    import os
    import requests
    import time
    import json

    access_id = 'fyekxcdka95atveo85xl'
    secret = 'f81bcd20b481499b82a48353d45811d3'
    device_id = '4834120498f4abfcc35a'

    t = str(round(time.time() * 1000))

    token = get_token(access_id, secret, t)


    link_str = access_id + token + t

    sign = get_sign(secret, link_str)


    endpoint = r'https://openapi.tuyaus.com'
    headers = {
        'client_id': access_id,
        'sign': sign,
        'sign_method': 'HMAC-SHA256',
        't': t,
        'access_token': token,
        # 'Content-Type': 'application/json'
    }
    

    url = '{}/v1.0/devices/{}'.format(endpoint, device_id)
    resp = requests.get(url, headers=headers)
    print('GET resp: ' + resp.text)
    response = json.loads(resp.text)
    result = response['result']
    for k,v in result.items():
        print('{}：{}'.format(k, v))