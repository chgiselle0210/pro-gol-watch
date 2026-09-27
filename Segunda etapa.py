"""Avance 2 de Pro-Gol Watch: captura mediante clases y objetos."""

from decimal import Decimal, InvalidOperation
from pathlib import Path


ARCHIVO_SALIDA = Path(__file__).with_name("salida.txt")

MENSAJES = {
    "nomina": "Nómina en formato incorrecto. Debe capturar solo números y letras.",
    "usuario": "Nombre de usuario en formato incorrecto. Debe capturar solo letras.",
    "cantidad": "Cantidad de videos en formato incorrecto. Debe capturar solo números.",
    "titulo": "Título del video en formato incorrecto. Debe capturar solo números y letras.",
    "video": "Nombre del video en formato incorrecto. Debe capturar solo números y letras.",
    "extension": "Extensión del video en formato incorrecto. Debe capturar solo números y letras.",
    "tamano_formato": "Tamaño del video en formato incorrecto. Debe capturar solo números.",
    "tamano_limite": "El archivo no debe pesar más de 3 MB",
}


def mostrar_mensaje(clave):
    """Muestra los mensajes de validación desde una única función."""
    print(MENSAJES[clave])


def validar_alfanumerico(valor):
    """Valida una cadena compuesta únicamente por letras y números."""
    return bool(valor) and valor.isalnum()


def validar_nombre(valor):
    """Valida nombres de personas con letras y espacios."""
    return bool(valor) and all(parte.isalpha() for parte in valor.split())


def validar_texto_video(valor):
    """Valida títulos y nombres de videos con letras, números y espacios."""
    return bool(valor) and all(
        caracter.isalnum() or caracter.isspace() for caracter in valor
    )


def pedir_texto(indicacion, validador, mensaje):
    """Repite la captura hasta que el texto sea válido."""
    while True:
        valor = input(indicacion).strip()
        if validador(valor):
            return valor
        mostrar_mensaje(mensaje)


def pedir_cantidad():
    """Solicita un número entero de videos igual o mayor que uno."""
    while True:
        valor = input("Cantidad de videos a subir: ").strip()
        if not valor.isdecimal():
            mostrar_mensaje("cantidad")
            continue

        cantidad = int(valor)
        if cantidad < 1:
            print("Debes subir al menos 1 video.")
            continue

        return cantidad


def manejar_excepcion(error):
    """Distingue errores de formato y errores por tamaño fuera del límite."""
    if isinstance(error, InvalidOperation):
        mostrar_mensaje("tamano_formato")
    elif isinstance(error, ValueError):
        mostrar_mensaje("tamano_limite")


def pedir_tamano():
    """Captura un tamaño numérico mayor que cero y de hasta 3 MB."""
    while True:
        texto = input("Tamaño del video en MB: ").strip()
        try:
            tamano = Decimal(texto)
            if not tamano.is_finite():
                raise InvalidOperation()
            if not 0 < tamano <= 3:
                raise ValueError("Tamaño fuera del límite")
            return tamano
        except (InvalidOperation, ValueError) as error:
            manejar_excepcion(error)


def pedir_respuesta(indicacion):
    """Solicita y normaliza una respuesta Sí o No."""
    while True:
        respuesta = input(indicacion).strip().casefold()
        if respuesta in ("si", "sí", "s"):
            return True
        if respuesta in ("no", "n"):
            return False
        print("Responde Sí o No.")


class Persona:
    """Representa a la persona que registra los videos."""

    def __init__(self):
        """Inicializa los atributos de la persona."""
        self.nombre = ""
        self.id_nomina = ""

    def capturar_nombre(self):
        """Captura y valida el nombre."""
        self.nombre = pedir_texto(
            "Nombre del usuario: ", validar_nombre, "usuario"
        )

    def capturar_id(self):
        """Captura y valida el número de nómina."""
        self.id_nomina = pedir_texto(
            "Número de nómina: ", validar_alfanumerico, "nomina"
        )

    def imprimir_nombre(self):
        """Imprime el nombre almacenado."""
        print(f"Nombre del usuario: {self.nombre}")

    def imprimir_id(self):
        """Imprime la nómina almacenada."""
        print(f"Número de nómina: {self.id_nomina}")


class Videos:
    """Representa un video relacionado con una persona."""

    def __init__(self):
        """Inicializa título, nombre, extensión y tamaño."""
        self.titulo = ""
        self.nombre = ""
        self.extension = ""
        self.tamano = Decimal("0")

    def capturar_titulo(self):
        """Captura el título requerido por la primera etapa."""
        self.titulo = pedir_texto(
            "Título del video: ", validar_texto_video, "titulo"
        )

    def capturar_nombre(self):
        """Captura y valida el nombre del video."""
        self.nombre = pedir_texto(
            "Nombre del video: ", validar_texto_video, "video"
        )

    def capturar_extension(self):
        """Captura la extensión con o sin punto inicial."""
        while True:
            extension = input(
                "Extensión del video (ejemplo: .mp4): "
            ).strip()
            sin_punto = extension[1:] if extension.startswith(".") else extension

            if validar_alfanumerico(sin_punto):
                self.extension = "." + sin_punto.lower()
                return

            mostrar_mensaje("extension")

    def capturar_tamano(self):
        """Captura y valida el tamaño del video."""
        self.tamano = pedir_tamano()

    def imprimir_nombre(self):
        """Imprime el nombre del video."""
        print(f"Nombre del video: {self.nombre}")

    def imprimir_extension(self):
        """Imprime la extensión del video."""
        print(f"Extensión del video: {self.extension}")

    def imprimir_tamano(self):
        """Imprime el tamaño del video en MB."""
        print(f"Tamaño del video: {format(self.tamano, 'f')} MB")

    def imprimir_datos(self):
        """Imprime todos los datos del video."""
        print(f"Título del video: {self.titulo}")
        self.imprimir_nombre()
        self.imprimir_extension()
        self.imprimir_tamano()


def capturar_persona_y_cantidad():
    """Crea el objeto Persona y captura los datos iniciales."""
    persona = Persona()
    persona.capturar_id()
    persona.capturar_nombre()
    cantidad = pedir_cantidad()
    return persona, cantidad


def capturar_videos(cantidad):
    """Crea y captura un objeto Videos por cada video solicitado."""
    videos = []

    for numero in range(1, cantidad + 1):
        print(f"\n--- Video {numero} ---")
        video = Videos()
        video.capturar_titulo()
        video.capturar_nombre()
        video.capturar_extension()
        video.capturar_tamano()
        videos.append(video)

    return videos


def guardar_salida(persona, cantidad, videos):
    """Guarda la persona y todos sus videos en una sola línea."""
    campos = [persona.id_nomina, persona.nombre, str(cantidad)]

    for video in videos:
        campos.extend(
            [
                video.titulo,
                video.nombre,
                video.extension,
                format(video.tamano, "f"),
            ]
        )

    linea = " | ".join(campos) + " |\n"

    with ARCHIVO_SALIDA.open("a", encoding="utf-8") as archivo:
        archivo.write(linea)

    print(f"\nInformación guardada en: {ARCHIVO_SALIDA}")


def main():
    """Ejecuta el mismo flujo del avance 1 mediante objetos."""
    print("=== Pro-Gol Watch | Segunda etapa ===")

    while True:
        persona, cantidad = capturar_persona_y_cantidad()

        print(
            f"\nBienvenido/a {persona.nombre}, tu número de nómina es "
            f"{persona.id_nomina} y estás intentando subir {cantidad} "
            f"{'video' if cantidad == 1 else 'videos'}."
        )

        if pedir_respuesta("¿Es correcta la información? Sí/No: "):
            videos = capturar_videos(cantidad)

            print("\n--- Resumen de la captura ---")
            persona.imprimir_id()
            persona.imprimir_nombre()
            print(f"Cantidad de videos: {cantidad}")

            for numero, video in enumerate(videos, start=1):
                print(f"\nVideo {numero}:")
                video.imprimir_datos()

            guardar_salida(persona, cantidad, videos)
            print("Muchas gracias por haber usado nuestro sistema, hasta pronto.")
            return

        if pedir_respuesta("¿Deseas salir del sistema? Sí/No: "):
            print("Muchas gracias por haber usado nuestro sistema, hasta pronto.")
            return

        print("\nCaptura nuevamente tus datos.\n")


if __name__ == "__main__":
    main()