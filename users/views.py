from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (
    UserRegisterForm,
    ProfileUpdateForm,
    UserUpdateForm,
)
from django.contrib.auth import logout , update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm


def register_user(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created successfully for {username}")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def logout_user(request):
    logout(request)
    return redirect("logout_view")


def logout_view(request):
    return render(request, "users/logout_view.html")


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            username = user_form.cleaned_data.get("username")
            messages.success(request, f"User updated for {username}")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "users/profile.html", context)

@login_required
def reset_password(request):
    if request.method == "POST":
        reset_form = PasswordChangeForm(request.user, request.POST)
        if reset_form.is_valid():
            try:
                reset_form.save()
                update_session_auth_hash(request, reset_form.user)
                messages.success(request, "Password changed successfully")
                return redirect('blog-home')
            except ValidationError as error:
                messages.error(request, ','.join(error))
                return redirect('reset-password')
    else:
        reset_form = PasswordChangeForm(request.user)

    return render(request, "users/reset_password.html", {"form": reset_form})