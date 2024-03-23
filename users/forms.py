# from socket import fromshare
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UsersamProfileForm(forms.ModelForm):
    # image = forms.ImageField()
    # grade = forms.CharField(max_length=100)
    # phonenumber = forms.CharField(max_length=20)
    # gender = forms.ChoiceField(choices=[("male", "Male"), ("female", "Female")])

    class Meta:
        model = samaritanProfile
        fields = [
            "image",
            "grade",
            "occupation",
            "age",
            "phonenumber",
            "gender",
            "address",
        ]


class UserdisProfileForm(forms.ModelForm):
    disability_CHOICES = [
        ("dyslexia", "Dyslexia"),
    ]

    # image = forms.ImageField()
    # rade = forms.CharField(max_length=100)
    # phonenumber = forms.CharField(max_length=20)
    # gender = forms.ChoiceField(choices=[("male", "Male"),("female", "Female"),])
    disabilities = forms.MultipleChoiceField(
        choices=disability_CHOICES, widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = disabilityProfile
        fields = [
            "image",
            "grade",
            "age",
            "phonenumber",
            "phonenumber",
            "state",
            "gender",
            "disabilities",
        ]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


class disProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = disabilityProfile
        fields = [
            "image",
            "grade",
            "age",
            "phonenumber",
            "state",
            "city",
            "gender",
            "disabilities",
        ]


class samProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = samaritanProfile
        fields = [
            "image",
            "grade",
            "occupation",
            "age",
            "phonenumber",
            "gender",
            "address",
        ]
