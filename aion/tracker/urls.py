from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/item/<int:pk>/", views.item_api),
]
