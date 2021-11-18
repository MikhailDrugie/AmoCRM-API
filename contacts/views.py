from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests
from contacts.models import AccessToken, Contact
from .forms import NewContact
import json

with open('static/config.json') as config_file:
    subdomain = json.load(config_file)['subdomain']
link_contacts = 'https://' + subdomain + '.amocrm.ru/api/v4/contacts'
link_leads = 'https://' + subdomain + '.amocrm.ru/api/v4/leads'


def header():
    if AccessToken.objects.filter(id=1).exists():
        return {
            'Authorization': 'Bearer ' + AccessToken.objects.get(id=1).token
        }


def get_contacts(link, headers):
    c = Contact.objects.all()
    c.delete()
    contacts = requests.get(link, headers=headers)
    if str(contacts) == '<Response [204]>':
        return "Нет контактов :("
    elif '_embedded' not in contacts.json():
        return "Нужно перезагрузить сервер?"
    else:
        contacts = contacts.json()['_embedded']['contacts']
        for contact in contacts:
            c = Contact(id=contact['id'], name=contact['name'])
            for i in contact['custom_fields_values']:
                if i['field_code'] == 'EMAIL':
                    c.email = i['values'][0]['value']
                elif i['field_code'] == 'PHONE':
                    c.phone = i['values'][0]['value']
                c.save()
        return "Контакты успешно обновлены!"


def new_json(contact):
    return [{
        "name": contact['name'],
        "custom_fields_values": [
            {
                "field_id": 414349,
                "field_name": "Телефон",
                "field_code": "PHONE",
                "field_type": "multitext",
                "values": [
                    {
                        "value": contact['phone'],
                        "enum_id": 200811,
                        "enum_code": "WORK"
                    }
                ]
            },
            {
                "field_id": 414351,
                "field_name": "Email",
                "field_code": "EMAIL",
                "field_type": "multitext",
                "values": [
                    {
                        "value": contact['email'],
                        "enum_id": 200823,
                        "enum_code": "WORK"
                    }
                ]
            }
        ]
    }]


def phone_json(phone, _id):
    return [{
        "id": _id,
        "custom_fields_values": [
            {
                "field_id": 414349,
                "field_name": "Телефон",
                "field_code": "PHONE",
                "field_type": "multitext",
                "values": [
                    {
                        "value": phone,
                        "enum_id": 200811,
                        "enum_code": "WORK"
                    }
                ]
            }
        ]
    }]


def email_json(email, _id):
    return [{
        "id": _id,
        "custom_fields_values": [
            {
                "field_id": 414351,
                "field_name": "Email",
                "field_code": "EMAIL",
                "field_type": "multitext",
                "values": [
                    {
                        "value": email,
                        "enum_id": 200823,
                        "enum_code": "WORK"
                    }
                ]
            }
        ]
    }]


def leads_json(_id):
    return [{
        "_embedded": {
            "contacts": [
                {"id": _id,
                 "is_main": True}
            ]
        }
    }]


def post_patch(act, _json, link, headers):
    if act == 'patch':
        return requests.patch(link, headers=headers, json=_json).json()
    elif act == 'post':
        return requests.post(link, headers=headers, json=_json).json()


def index(request):
    contacts = Contact.objects.values()
    if request.method == 'POST':
        form = NewContact(request.POST)
        if form.is_valid():
            c = form.cleaned_data
            action = 'patch'
            if Contact.objects.filter(name=c['name'], phone=c['phone']).exists():
                data = email_json(c['email'], Contact.objects.get(name=c['name'], phone=c['phone']).id)
            elif Contact.objects.filter(name=c['name'], email=c['email']).exists():
                data = phone_json(c['phone'], Contact.objects.get(name=c['name'], email=c['email']).id)
            else:
                action = 'post'
                data = new_json(c)
            response = post_patch(action, data, link_contacts, header())
            _id = response['_embedded']['contacts'][0]['id']
            leads_data = leads_json(_id)
            post_patch('post', leads_data, link_leads, header())
            return HttpResponseRedirect('/contacts/upd/')
    else:
        form = NewContact()
    return render(
        request,
        'index.html',
        context={'display_contacts': contacts,
                 'form': form}
    )


def update(request):
    response = get_contacts(link_contacts, header())
    return render(
        request,
        'updated.html',
        context={'response': response}
    )
