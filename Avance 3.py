"""Avance 3: captura con clases y almacenamiento en Django/PostgreSQL."""

import getpass
import os
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

# Se ubica el proyecto Django y el archivo de la segunda etapa.
BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_ETAPA_2 = BASE_DIR / "Segunda etapa.py"

# Se cargan las clases y funciones del avance anterior.
especificacion = spec_from_file_location("segunda_etapa", ARCHIVO_ETAPA_2)
modulo_etapa_2 = module_from_spec(especificacion)
especificacion.loader.exec_module(modulo_etapa_2)

# Se configura Django antes de importar los modelos.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mis_videos.settings")

# Se solicita la contraseña sin mostrarla si esta terminal no la tiene.
if not os.environ.get("PG_PASSWORD"):
    os.environ["PG_PASSWORD"] = getpass.getpass(
        "Contraseña local de PostgreSQL: "
    )

import django

django.setup()

from django.core.files import File
from django.db import transaction
from videos.models import Persona as PersonaBD
from videos.models import Video as VideoBD
from videos.models import VideoUsuario


LIMITE_BYTES = 3 * 1024 * 1024


def pedir_archivo(video):
    """Solicita un video existente con la extensión y tamaño permitidos."""
    while True:
        texto = input(
            f"Ruta completa del archivo para '{video.titulo}': "
        ).strip().strip('"')
        ruta = Path(texto).expanduser()

        if not ruta.is_file():
            print("No existe ese archivo. Copia su ruta completa e inténtalo de nuevo.")
            continue

        if ruta.suffix.lower() != video.extension.lower():
            print(f"El archivo debe tener la extensión {video.extension}.")
            continue

        tamano_bytes = ruta.stat().st_size

        if tamano_bytes == 0 or tamano_bytes > LIMITE_BYTES:
            print("El archivo debe pesar más de 0 y no más de 3 MB.")
            continue

        tamano_real = tamano_bytes / (1024 * 1024)
        if abs(tamano_real - float(video.tamano)) > 0.02:
            print(
                f"El archivo pesa {tamano_real:.2f} MB; captura ese tamaño "
                "en los datos del video."
            )
            continue

        return ruta


def guardar_en_postgresql(persona, videos_y_rutas):
    """Guarda usuario, videos y asociaciones en una transacción."""
    with transaction.atomic():
        usuario, _ = PersonaBD.objects.update_or_create(
            nomina=persona.id_nomina,
            defaults={"nombre": persona.nombre},
        )

        for video, ruta in videos_y_rutas:
            with ruta.open("rb") as archivo:
                registro = VideoBD(
                    titulo=video.titulo,
                    nombre=video.nombre,
                    extension=video.extension,
                    tamano_mb=video.tamano,
                )
                registro.archivo = File(archivo, name=ruta.name)
                registro.full_clean()
                registro.save()

            VideoUsuario.objects.create(
                usuario=usuario,
                video=registro,
            )

            print(
                f"Guardado en PostgreSQL: {registro.titulo} "
                f"(ID {registro.pk})"
            )


def main():
    """Captura datos mediante objetos y los guarda en el proyecto Django."""
    print("=== Pro-Gol Watch | Avance 3 ===")

    while True:
        persona, cantidad = modulo_etapa_2.capturar_persona_y_cantidad()

        print(
            f"\nBienvenido/a {persona.nombre}, tu número de nómina es "
            f"{persona.id_nomina} y estás intentando subir {cantidad} "
            f"{'video' if cantidad == 1 else 'videos'}."
        )

        if modulo_etapa_2.pedir_respuesta(
            "¿Es correcta la información? Sí/No: "
        ):
            break

        if modulo_etapa_2.pedir_respuesta(
            "¿Deseas salir del sistema? Sí/No: "
        ):
            print(
                "Muchas gracias por haber usado nuestro sistema, "
                "hasta pronto."
            )
            return

        print("\nCaptura nuevamente tus datos.\n")

    videos_y_rutas = []

    for numero in range(1, cantidad + 1):
        print(f"\n--- Video {numero} ---")
        video = modulo_etapa_2.Videos()
        video.capturar_titulo()
        video.capturar_nombre()
        video.capturar_extension()
        video.capturar_tamano()
        ruta = pedir_archivo(video)
        videos_y_rutas.append((video, ruta))

    guardar_en_postgresql(persona, videos_y_rutas)

    print(
        "\nRegistro completado. Abre http://127.0.0.1:8000/videos/ "
        "para comprobarlo en la biblioteca."
    )


if __name__ == "__main__":
    main()