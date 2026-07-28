from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("saved/", views.event_saved, name="event_saved"),
    path("<int:event_id>/", views.event_detail, name="event_detail"),
    path(
        "<int:event_id>/favorite/",
        views.event_toggle_favorite,
        name="event_toggle_favorite",
    ),
    path("create/", views.event_create, name="event_create"),
    path("<int:event_id>/edit/", views.event_edit, name="event_edit"),
    path("<int:event_id>/delete/", views.event_delete, name="event_delete"),
]
