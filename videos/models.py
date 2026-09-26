from pathlib import Path

from django.core.exceptions import ValidationError
from django.db import models


MAX_VIDEO_BYTES = 3 * 1024 * 1024
EXTENSIONES_PERMITIDAS = {".mp4", ".mov", ".mpg", ".mpeg", ".webm"}


def validar_archivo_video(archivo):
    extension = Path(archivo.name).suffix.lower()

    if extension not in EXTENSIONES_PERMITIDAS:
        raise ValidationError(
            "Extensión del video en formato incorrecto. "
            "Usa mp4, mov, mpg, mpeg o webm."
        )

    if archivo.size > MAX_VIDEO_BYTES:
        raise ValidationError("El archivo no debe pesar más de 3 MB.")


class Persona(models.Model):
    nomina = models.CharField(
        primary_key=True,
        max_length=10,
        verbose_name="Número de nómina",
    )
    nombre = models.CharField(max_length=50, verbose_name="Nombre completo")

    class Meta:
        db_table = "TBL_Usuario"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.nombre} ({self.nomina})"


class Video(models.Model):
    titulo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=50)
    extension = models.CharField(max_length=5)
    tamano_mb = models.DecimalField(max_digits=4, decimal_places=2)
    archivo = models.FileField(
        upload_to="videos/",
        validators=[validar_archivo_video],
    )
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "TBL_Video"
        ordering = ["-fecha_subida"]

    def __str__(self):
        return self.titulo


class VideoUsuario(models.Model):
    usuario = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name="videos_relacionados",
        db_column="nomina_usuario",
    )
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name="usuarios_relacionados",
    )

    class Meta:
        db_table = "TBL_Usuario_Video"
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "video"],
                name="usuario_video_unico",
            )
        ]

    def __str__(self):
        return f"{self.usuario.nomina} → {self.video.titulo}"