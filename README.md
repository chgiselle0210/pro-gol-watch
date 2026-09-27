# Pro-Gol Watch

Proyecto final de mi curso **Backend con Python/Django**. Con esta aplicación se puede registrar usuarios, subir videos de hasta 3 MB, consultarlos en una biblioteca, reproducirlos y descargarlos. Utilicé Python, Django, PostgreSQL, HTML y CSS.

## Funcionalidades

- Captura de número de nómina, nombre y cantidad de videos.
- Confirmación de los datos antes de continuar.
- Validación de los campos y del tamaño y extensión de cada archivo.
- Almacenamiento de usuarios, videos y sus relaciones en PostgreSQL.
- Biblioteca con opciones para reproducir y descargar los videos.
- Programas de consola correspondientes a las tres primeras etapas del proyecto.

## Requisitos

- Python 3.12 o superior.
- PostgreSQL instalado y en ejecución.
- Las dependencias de `requirements.txt`.

## Instalación en Windows con PowerShell

Desde la carpeta del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Se debe crear en PostgreSQL una base de datos llamada `Pro_Gol`.

La configuración que desarrollé para el proyecto utiliza el usuario local `postgres` y obtiene su contraseña de la variable de entorno `PG_PASSWORD`. En PowerShell, se puede introducir sin mostrarla así:

```powershell
$clave = Read-Host "Contraseña local de PostgreSQL" -AsSecureString
$env:PG_PASSWORD = [System.Net.NetworkCredential]::new("", $clave).Password
```

Después, crear las tablas e iniciar el servidor:

```powershell
python manage.py migrate
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/`.

> La contraseña de PostgreSQL y los videos cargados no las incluí en el repositorio. Cada instalación debe configurar su propia base de datos.

## Etapas del proyecto

| Etapa | Archivo o componente | Resultado |
|---|---|---|
| 1 | `Primera etapa.py` | Captura y validación en consola; genera `salida.txt`. |
| 2 | `Segunda etapa.py` | Usa las clases `Persona` y `Videos`; registra datos en `salida.txt`. |
| 3 | `Avance 3.py` y modelos Django | Guarda usuarios, archivos de video y relaciones en PostgreSQL. |
| 4 | Aplicación web Django | Formularios HTML, validaciones, estilos CSS y biblioteca de videos. |

Para ejecutar las etapas de consola:

```powershell
python "Primera etapa.py"
python "Segunda etapa.py"
python "Avance 3.py"
```

La tercera etapa solicita la ruta local de un video real de hasta 3 MB. Requiere que la base `Pro_Gol` exista y que se hayan aplicado las migraciones.

## Base de datos

Los modelos Django crean las tablas `TBL_Usuario`, `TBL_Video` y `TBL_Usuario_Video`. Los archivos de video se guardan localmente en `media/videos/`; PostgreSQL conserva sus datos y relaciones.

## Prueba realizada

Revisé la captura de datos, la confirmación, la subida de un MP4 de 1.09 MB, su registro en PostgreSQL, su aparición en la biblioteca, su reproducción y su descarga. También ejecuté las etapas de consola y comprobé que se generara `salida.txt`.

## Autora

Giselle Cantú Chávez — proyecto académico de Tecmilenio.
