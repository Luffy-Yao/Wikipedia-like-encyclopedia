from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.page_content,  name = "page_content"),
    path("search/?q=", views.search, name = "search"),
    path("new/", views.new_page, name = "new_page"),
    path("random/", views.random_page, name = "random_page"),
    path("<str:title>/edit", views.edit,  name = "edit_page")
]
