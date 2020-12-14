from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tools/drop-calculator", views.drop_calculator, name="drop-calculator"),
]