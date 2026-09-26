from decimal import Decimal
from pathlib import Path

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.forms import formset_factory
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DatosUsuarioForm, DatosVideoForm
from .models import Persona, Video, VideoUsuario


def inicio(request):
    if request.method == "POST":
        form = DatosUsuarioForm(request.POST)
        if form.is_valid():
            request.session["datos_pendientes"] = form.cleaned_data
            return redirect("confirmar")
    else:
        form = DatosUsuarioForm()

    return render(request, "videos/inicio.html", {"form": form})


def confirmar(request):
    datos = request.session.get("datos_pendientes")
    if not datos:
        return redirect("inicio")

    if request.method == "POST":
        if request.POST.get("respuesta") == "si":
            return redirect("subir_videos")
        request.session.pop("datos_pendientes", None)
        return redirect("inicio")

    return render(request, "videos/confirmar.html", {"datos": datos})


def subir_videos(request):
    datos = request.session.get("datos_pendientes")
    if not datos:
        return redirect("inicio")

    cantidad = int(datos["cantidad"])
    ConjuntoVideos = formset_factory(
        DatosVideoForm,
        extra=cantidad,
        min_num=cantidad,
        max_num=cantidad,
        validate_min=True,
        validate_max=True,
    )

    if request.method == "POST":
        conjunto = ConjuntoVideos(request.POST, request.FILES)
        if conjunto.is_valid():
            with transaction.atomic():
                persona, _ = Persona.objects.update_or_create(
                    nomina=datos["nomina"],
                    defaults={"nombre": datos["nombre"]},
                )

                for formulario in conjunto:
                    info = formulario.cleaned_data
                    archivo = info["archivo"]
                    video = Video.objects.create(
                        titulo=info["titulo"],
                        nombre=info["nombre"],
                        extension=info["extension"],
                        tamano_mb=(
                            Decimal(archivo.size) / Decimal(1024 * 1024)
                        ).quantize(Decimal("0.01")),
                        archivo=archivo,
                    )
                    VideoUsuario.objects.create(usuario=persona, video=video)

            request.session.pop("datos_pendientes", None)
            messages.success(
                request,
                f"Se guardaron correctamente {cantidad} videos.",
            )
            return redirect("lista_videos")
    else:
        conjunto = ConjuntoVideos()

    return render(
        request,
        "videos/subir.html",
        {"conjunto": conjunto, "datos": datos},
    )


def lista_videos(request):
    relaciones = VideoUsuario.objects.select_related(
        "usuario", "video"
    ).order_by("-video__fecha_subida")
    return render(
        request,
        "videos/lista.html",
        {"relaciones": relaciones},
    )


def reproducir_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if not video.archivo:
        raise Http404("El video no tiene archivo.")

    respuesta = FileResponse(
        video.archivo.open("rb"),
        content_type=_tipo_video(video.extension),
    )
    respuesta["Content-Disposition"] = (
        f'inline; filename="{Path(video.archivo.name).name}"'
    )
    return respuesta


def descargar_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if not video.archivo:
        raise Http404("El video no tiene archivo.")

    return FileResponse(
        video.archivo.open("rb"),
        as_attachment=True,
        filename=Path(video.archivo.name).name,
        content_type=_tipo_video(video.extension),
    )


def _tipo_video(extension):
    return {
        ".mp4": "video/mp4",
        ".mov": "video/quicktime",
        ".mpg": "video/mpeg",
        ".mpeg": "video/mpeg",
        ".webm": "video/webm",
    }.get(extension, "application/octet-stream")