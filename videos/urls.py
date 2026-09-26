from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("confirmar/", views.confirmar, name="confirmar"),
    path("subir/", views.subir_videos, name="subir_videos"),
    path("videos/", views.lista_videos, name="lista_videos"),
    path(
        "videos/<int:video_id>/ver/",
        views.reproducir_video,
        name="reproducir_video",
    ),
    path(
        "videos/<int:video_id>/descargar/",
        views.descargar_video,
        name="descargar_video",
    ),
]