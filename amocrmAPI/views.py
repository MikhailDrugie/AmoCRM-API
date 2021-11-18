from django.contrib.sites import requests
from django.shortcuts import render
import requests
import json
from contacts.models import AccessToken, RefreshToken

with open('static/config.json') as config_file:
    config = json.load(config_file)
    subdomain = config['subdomain']
    client_secret = config['client_secret']
    client_id = config['client_id']
    url = config['url']


def tokens(request, first=False, ref_code=None):
    grant_type = "refresh_token"
    ref_or_code = grant_type
    if first:
        grant_type = "authorization_code"
        ref_or_code = "code"
        print('Access code is', request.GET['code'])
        ref_code = request.GET['code']
    response = requests.post('https://' + subdomain + '.amocrm.ru/oauth2/access_token', data={
        "client_id": client_id, "client_secret": client_secret, "grant_type": grant_type,
        ref_or_code: ref_code, "redirect_uri": "https://" + url})
    with open('static/token.json', 'w', encoding='utf-8') as token_file:
        json.dump(response.json(), token_file, indent=2, ensure_ascii=False)
    a_token = AccessToken(id=1, token=response.json()["access_token"])
    a_token.save()
    r_token = RefreshToken(id=1, token=response.json()["refresh_token"])
    r_token.save()
    print("Access token is", response.json()["access_token"] + '\n' +
          "Refresh token is", response.json()["refresh_token"])


def welcome(request):
    if 'code' in request.GET:
        tokens(request, first=True)
    return render(
        request,
        'welcome.html',
    )


def refreshing(request):
    refresh = RefreshToken.objects.get(id=1)
    tokens(request, ref_code=refresh.token)
    return render(
        request,
        'refreshed.html')
