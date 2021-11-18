import os
import json
import requests


def host_name():
    os.system("curl  http://localhost:4040/api/tunnels > static/url.json")

    with open('static/url.json') as data_file:
        datajson = json.load(data_file)
    msg = ''
    for i in datajson['tunnels']:
        msg += ' ' + i['public_url']
    return sorted(msg.split())[0][7:]


flag = True
response = 'Ngrok не включён!'
try:
    response = requests.get('http://localhost:4040/inspect/http')
except requests.exceptions.ConnectionError:
    flag = False
finally:
    print(response)
if flag:
    check = input("Нужно ли вводить данные? (y/n)  ")
    if check == 'y':
        AMO_SUBDOMAIN = input("Введите ваш поддомен (то, что идёт перед .amocrm.ru/: ")
        URL = host_name()
        print("https://" + URL + '\n' +
              'Поместите данную ссылку в виджет https://' + AMO_SUBDOMAIN +
              '.amocrm.ru/settings/widgets/ и перезапустите его после запуска manage.py.')
        AMO_S_KEY = input("Введите секретный ключ из виджета: ")
        ID = input("Введите ваш клиентский ID из виджета: ")
        with open("static/config.json", "w") as f:
            json.dump({"subdomain": AMO_SUBDOMAIN, "url": URL, "client_secret": AMO_S_KEY,
                       "client_id": ID}, f)
    else:
        with open('static/config.json') as config_file:
            config = json.load(config_file)
        config["url"] = host_name()
        with open('static/config.json', 'w') as f:
            json.dump(config, f)
        print("https://" + config["url"] + '\n' +
              'Поместите данную ссылку в виджет https://' + config["subdomain"] +
              '.amocrm.ru/settings/widgets/ и перезапустите его после запуска manage.py для получения токенов.')
