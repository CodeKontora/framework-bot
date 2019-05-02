import requests
import json


def get_proxy():
    url = 'http://pubproxy.com/api/proxy?type=https'
    response = requests.get(url)

    # Если адрес забанили или превышен лимит на запросы
    try:
        json_proxy = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        last_proxy = {'ip_port': read_proxy()}
        return last_proxy

    # Создаём словарь с данными о прокси
    proxy_data = dict.fromkeys(['ip_port', 'ip', 'port', 'country', 'last_check'])

    proxy_data['ip_port'] = json_proxy['data'][0]['ipPort']
    proxy_data['ip'] = json_proxy['data'][0]['ip']
    proxy_data['port'] = json_proxy['data'][0]['port']
    proxy_data['country'] = json_proxy['data'][0]['country']
    proxy_data['last_check'] = json_proxy['data'][0]['last_checked']

    return proxy_data


def write_proxy(proxy):
    file = open('proxy.txt', 'w')
    file.write('{}'.format(proxy['ip_port']))
    file.close()


def read_proxy():
    file = open('proxy.txt', 'r')
    ip_port = file.read()
    file.close()

    return ip_port
