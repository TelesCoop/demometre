from django.urls import path

from . import views

app_name = "my_auth"
urlpatterns = [
    path("edit", views.edit_user, name="edit_user"),
    path("login", views.frontend_login),
    path("logout", views.frontend_logout),
    path("profile", views.who_am_i, name="auth_profile"),
    path("signup", views.frontend_signup),
    path("user/reset-password-link", views.front_end_reset_password_link),
    path("user/reset-password", views.front_end_reset_password),
    path("unknown-user", views.front_end_create_unknown_user),
]
