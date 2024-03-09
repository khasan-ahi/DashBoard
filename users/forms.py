from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class MyUserCreationForm(UserCreationForm):

    username = forms.CharField(label='Name', min_length=5, max_length=150)

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"class": "form-control form-control-user",
                                                     "placeholder": "Имя пользователя"})
        self.fields['password1'].widget.attrs.update({"class": "form-control form-control-user",
                                                     "placeholder": "Введите пароль"})
        self.fields['password2'].widget.attrs.update({"class": "form-control form-control-user",
                                                     "placeholder": "Повторите пароль"})

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
