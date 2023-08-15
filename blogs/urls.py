from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>/post", views.show_post, name="show_post"),
    path("post/create", views.create_post, name="create_post"),
    path("<int:id>/edit", views.update_post, name="update_post"),
    path("<int:id>/delete", views.destroy_post, name="delete_post"),
    path("categories/", views.categories, name="categories"),
    path("category/<str:name>", views.category_post, name="category_post")
]