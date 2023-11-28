from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("process_csv/", views.process_csv, name="process_csv"),
]