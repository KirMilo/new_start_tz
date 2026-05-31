from django.urls import path
from . import views

app_name = "items"
urlpatterns = [
    path('', views.items_list_view, name="items_list")
]