from django.urls import path
from . import views

urlpatterns = [
    path("login", views.log_in, name="login"),
    path("logout", views.log_out, name="logout"),
    path("signup", views.sign_up, name="signup"),
    path("", views.get_rifle_list, name="rifle_list"),
    path("<str:name>", views.rifle, name="rifle_by_name"),
]