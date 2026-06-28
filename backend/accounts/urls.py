from django.urls import path

from .views import (
    accounts_home,
    register_user,
    login_user,
    user_profile,
    logout_user,
)


urlpatterns = [
    path("", accounts_home, name="accounts-home"),
    path("register/", register_user, name="register-user"),
    path("login/", login_user, name="login-user"),
    path("profile/", user_profile, name="user-profile"),
    path("logout/", logout_user, name="logout-user"),
]