from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *


def samregister(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        form1 = UsersamProfileForm(request.POST)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            try:
                user_profile = samaritanProfile.objects.get(user=user)
                # If a profile already exists, update it
                user_profile.image = form1.cleaned_data["image"]
                user_profile.grade = form1.cleaned_data["grade"]
                user_profile.phonenumber = form1.cleaned_data["phonenumber"]
                user_profile.age = form1.cleaned_data["age"]
                user_profile.address = form1.cleaned_data["address"]
                user_profile.gender = form1.cleaned_data["gender"]
                user_profile.disablities = form1.cleaned_data["disablities"]
                user_profile.save()
            except samaritanProfile.DoesNotExist:
                user_profile = form1.save(commit=False)
                user_profile.user = user
                user_profile.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account Created for {username}!")
            return redirect("login")
    else:
        form = UserRegisterForm()
        form1 = UsersamProfileForm
    return render(request, "users/samregister.html", {"form": form, "form1": form1})


def disregister(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        form1 = UserdisProfileForm(request.POST)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            try:
                user_profile = disabilityProfile.objects.get(user=user)
                # If a profile already exists, update it
                user_profile.image = form1.cleaned_data["image"]
                user_profile.grade = form1.cleaned_data["grade"]
                user_profile.phonenumber = form1.cleaned_data["phonenumber"]
                user_profile.gender = form1.cleaned_data["gender"]
                user_profile.state = form1.cleaned_data["state"]
                user_profile.city = form1.cleaned_data["city"]
                user_profile.disablities = form1.cleaned_data["disablities"]
                user_profile.save()
            except disabilityProfile.DoesNotExist:
                user_profile = form1.save(commit=False)
                user_profile.user = user
                user_profile.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account Created for {username}!")
            return redirect("login")
    else:
        form = UserRegisterForm()
        form1 = UserdisProfileForm
    return render(request, "users/disregister.html", {"form": form, "form1": form1})


# Create your views here.
@login_required
def samprofile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = samProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.samaritanprofile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Account Updated")
            return redirect("samprofile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = samProfileUpdateForm(instance=request.user.samaritanprofile)
    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/samprofile.html", context)


def disprofile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = disProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.disabilityprofile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Account Updated")
            return redirect("disprofile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = disProfileUpdateForm(instance=request.user.disabilityprofile)
    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/disprofile.html", context)
