# pylint: disable=relative-beyond-top-level

"""Views"""
from typing import Any, Dict, Union
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.contrib.auth.forms import PasswordChangeForm
from .forms import (
    UserRegisterForm,
    ProfileUpdateForm,
    UserUpdateForm,
)


def register_user(request: HttpRequest) -> Any:
    """Registers user"""
    if request.method == "POST":
        form: UserRegisterForm = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username: str = form.cleaned_data.get("username")
            messages.success(request, f"Account created successfully for {username}")
            return redirect("login")
    else:
        form: UserRegisterForm = UserRegisterForm()
    return render(request, "users/register.html", {"form": form, "title": "Register"})


@login_required
def logout_user(request: Any) -> Any:
    """Runs the logout func and redirecting to the logout view"""
    logout(request)
    return redirect("logout_view")


def logout_view(request: Any) -> Any:
    """Renders The Logout view after log out"""
    return render(request, "users/logout_view.html", {"title": "Log out"})


@login_required
def profile(request: HttpRequest) -> Any:
    """Shows the profile user if request is post it updates the profile"""
    if request.method == "POST":
        user_form: UserUpdateForm = UserUpdateForm(request.POST, instance=request.user)
        profile_form: ProfileUpdateForm = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            username: str = user_form.cleaned_data.get("username")
            messages.success(request, f"User updated for {username}")
            return redirect("profile")
    else:
        user_form: UserUpdateForm = UserUpdateForm(instance=request.user)
        profile_form: ProfileUpdateForm = ProfileUpdateForm(
            instance=request.user.profile
        )
    context: Dict[str, Union[str, UserRegisterForm, ProfileUpdateForm]] = {
        "user_form": user_form,
        "profile_form": profile_form,
        "title": "Profile",
    }
    return render(request, "users/profile.html", context)


@login_required
def reset_password(request: HttpRequest) -> Any:
    """Reset password if request is post"""
    if request.method == "POST":
        reset_form: PasswordChangeForm = PasswordChangeForm(request.user, request.POST)
        if reset_form.is_valid():
            try:
                reset_form.save()
                update_session_auth_hash(request, reset_form.user)
                messages.success(request, "Password changed successfully")
                return redirect("blog-home")
            except ValidationError as error:
                messages.error(request, ",".join(error))
                return redirect("reset-password")
    else:
        reset_form: PasswordChangeForm = PasswordChangeForm(request.user)

    return render(
        request,
        "users/reset_password.html",
        {"form": reset_form, "title": "Reset Password"},
    )
