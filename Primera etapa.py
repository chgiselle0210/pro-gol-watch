"""Avance 1 de Pro-Gol Watch: captura y validación en consola."""

from decimal import Decimal, InvalidOperation
from pathlib import Path


# Se define la ubicación del archivo de salida junto a este programa.
ARCHIVO_SALIDA = Path(__file__).with_name("salida.txt")

# Se agrupan los mensajes solicitados para mostrarlos desde una sola función.
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
    """Muestra el mensaje correspondiente a una validación."""
    print(MENSAJES[clave])


def validar_alfanumerico(valor):
    """Acepta letras y números, sin símbolos ni espacios."""
    return bool(valor) and valor.isalnum()


def validar_nombre(valor):
    """Acepta nombres con letras y espacios, como en el ejemplo del proyecto."""
    return bool(valor) and all(
        parte.isalpha() for parte in valor.split()
    )


def validar_texto_video(valor):
    """Acepta letras, números y espacios en títulos o nombres de videos."""
    return bool(valor) and all(
        caracter.isalnum() or caracter.isspace() for caracter in valor
    )


def pedir_texto(indicacion, validador, mensaje):
    """Solicita texto hasta recibir un valor válido."""
    while True:
        valor = input(indicacion).strip()
        if validador(valor):
            return valor
        mostrar_mensaje(mensaje)


def pedir_cantidad():
    """Solicita una cantidad entera de al menos un video."""
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


def pedir_datos_usuario():
    """Captura nómina, nombre y cantidad de videos."""
    nomina = pedir_texto(
        "Número de nómina: ", validar_alfanumerico, "nomina"
    )
    nombre = pedir_texto(
        "Nombre del usuario: ", validar_nombre, "usuario"
    )
    cantidad = pedir_cantidad()
    return nomina, nombre, cantidad


def manejar_excepcion(error):
    """Muestra el error adecuado cuando falla la captura del tamaño."""
    if isinstance(error, InvalidOperation):
        mostrar_mensaje("tamano_formato")
    elif isinstance(error, ValueError):
        mostrar_mensaje("tamano_limite")


def pedir_tamano():
    """Acepta números decimales mayores que cero y de hasta 3 MB."""
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


def pedir_datos_video(numero):
    """Captura y valida los datos de un video."""
    print(f"\n--- Video {numero} ---")
    titulo = pedir_texto(
        "Título del video: ", validar_texto_video, "titulo"
    )
    nombre = pedir_texto(
        "Nombre del video: ", validar_texto_video, "video"
    )

    # Se admite la extensión con o sin punto, como .mp4 o mp4.
    while True:
        extension = input("Extensión del video (ejemplo: .mp4): ").strip()
        if extension.startswith("."):
            extension_sin_punto = extension[1:]
        else:
            extension_sin_punto = extension

        if validar_alfanumerico(extension_sin_punto):
            extension = "." + extension_sin_punto.lower()
            break
        mostrar_mensaje("extension")

    tamano = pedir_tamano()
    return titulo, nombre, extension, tamano


def pedir_respuesta(indicacion):
    """Solicita una respuesta Sí o No."""
    while True:
        respuesta = input(indicacion).strip().casefold()
        if respuesta in ("si", "sí", "s"):
            return True
        if respuesta in ("no", "n"):
            return False
        print("Responde Sí o No.")


def guardar_salida(nomina, nombre, cantidad, videos):
    """Guarda todos los datos en una sola línea separada por barras."""
    campos = [nomina, nombre, str(cantidad)]

    for titulo, nombre_video, extension, tamano in videos:
        campos.extend(
            [titulo, nombre_video, extension, format(tamano, "f")]
        )

    linea = " | ".join(campos) + " |\n"

    # Se conserva un registro por línea si el programa se ejecuta varias veces.
    with ARCHIVO_SALIDA.open("a", encoding="utf-8") as archivo:
        archivo.write(linea)

    print(f"\nInformación guardada en: {ARCHIVO_SALIDA}")


def main():
    """Controla la confirmación y la captura de uno a N videos."""
    print("=== Pro-Gol Watch | Primera etapa ===")

    while True:
        nomina, nombre, cantidad = pedir_datos_usuario()

        print(
            f"\nBienvenido/a {nombre}, tu número de nómina es {nomina} "
            f"y estás intentando subir {cantidad} "
            f"{'video' if cantidad == 1 else 'videos'}."
        )

        if pedir_respuesta("¿Es correcta la información? Sí/No: "):
            videos = []
            for numero in range(1, cantidad + 1):
                videos.append(pedir_datos_video(numero))

            guardar_salida(nomina, nombre, cantidad, videos)
            print("Muchas gracias por haber usado nuestro sistema, hasta pronto.")
            return

        if pedir_respuesta("¿Deseas salir del sistema? Sí/No: "):
            print("Muchas gracias por haber usado nuestro sistema, hasta pronto.")
            return

        print("\nCaptura nuevamente tus datos.\n")


if __name__ == "__main__":
    main()