from django import forms


class NewContact(forms.Form):
    name = forms.CharField(label='Имя Фамилия', max_length=255, required=True)
    email = forms.CharField(label='Email', max_length=255, required=True)
    phone = forms.CharField(label='Телефон', max_length=255, required=True)
