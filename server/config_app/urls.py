from django.contrib import admin
from django.urls import include, path
from . import views

checkpatterns = [
    path("/user", views.check_user, name="user"),
    path("/nickname", views.check_nickname, name="nickname")
]

updatepatterns = [
    path("/nickname", views.update_nickname, name="nickname"),
    path("/email", views.update_email, name="email"),
    path("/phone", views.update_phone, name="phone")
]

deletepatterns = [
    path("/user", views.delete_user, name="user"),
]

urlpatterns = [
    path("admin", admin.site.urls),
    path("", views.index, name="index"),
    path("profile", views.profile, name="profile"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("check", include(checkpatterns), name="check"),
    path("update", include(updatepatterns), name="update"),
    path("delete", include(deletepatterns), name="delete"),
]