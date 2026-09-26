import re
from decimal import Decimal

from django import forms

from .models import EXTENSIONES_PERMITIDAS, MAX_VIDEO_BYTES


class DatosUsuarioForm(forms.Form):
    nomina = forms.CharField(
        label="Número de nómina",
        max_length=10,
        widget=forms.TextInput(attrs={"placeholder": "Ej. N087545"}),
    )
    nombre = forms.CharField(
        label="Nombre completo",
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Ej. Irma Guardado Segura"}),
    )
    cantidad = forms.IntegerField(
        label="Cantidad de videos",
        min_value=1,
        widget=forms.NumberInput(attrs={"min": "1"}),
    )

    def clean_nomina(self):
        valor = self.cleaned_data["nomina"].strip()
        if not re.fullmatch(r"[A-Za-z0-9]+", valor):
            raise forms.ValidationError(
                "Nómina en formato incorrecto. Debe capturar solo números y letras."
            )
        return valor

    def clean_nombre(self):
        valor = " ".join(self.cleaned_data["nombre"].split())
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+", valor):
            raise forms.ValidationError(
                "Nombre de usuario en formato incorrecto. Debe capturar solo letras."
            )
        return valor


class DatosVideoForm(forms.Form):
    titulo = forms.CharField(label="Título del video", max_length=100)
    nombre = forms.CharField(label="Nombre del video", max_length=50)
    extension = forms.ChoiceField(
        label="Extensión",
        choices=[
            (".mp4", ".mp4"),
            (".mov", ".mov"),
            (".mpg", ".mpg"),
            (".mpeg", ".mpeg"),
            (".webm", ".webm"),
        ],
    )
    tamano_mb = forms.DecimalField(
        label="Tamaño en MB",
        min_value=Decimal("0.01"),
        max_value=Decimal("3.00"),
        max_digits=4,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={"min": "0.01", "max": "3", "step": "0.01"}
        ),
    )
    archivo = forms.FileField(label="Archivo de video")

    def clean_titulo(self):
        valor = " ".join(self.cleaned_data["titulo"].split())
        if not re.fullmatch(r"[\wÁÉÍÓÚÜÑáéíóúüñ ,.\-]+", valor):
            raise forms.ValidationError(
                "Título del video en formato incorrecto. "
                "Debe capturar letras y números."
            )
        return valor

    def clean_nombre(self):
        valor = " ".join(self.cleaned_data["nombre"].split())
        if not re.fullmatch(r"[\wÁÉÍÓÚÜÑáéíóúüñ ,.\-]+", valor):
            raise forms.ValidationError(
                "Nombre del video en formato incorrecto. "
                "Debe capturar letras y números."
            )
        return valor

    def clean_archivo(self):
        archivo = self.cleaned_data["archivo"]
        extension = "." + archivo.name.rsplit(".", 1)[-1].lower()

        if extension not in EXTENSIONES_PERMITIDAS:
            raise forms.ValidationError(
                "Extensión del video en formato incorrecto."
            )
        if archivo.size > MAX_VIDEO_BYTES:
            raise forms.ValidationError("El archivo no debe pesar más de 3 MB.")
        if archivo.size == 0:
            raise forms.ValidationError("El archivo está vacío.")
        return archivo

    def clean(self):
        datos = super().clean()
        archivo = datos.get("archivo")
        extension = datos.get("extension")
        tamano_mb = datos.get("tamano_mb")

        if archivo and extension:
            extension_real = "." + archivo.name.rsplit(".", 1)[-1].lower()
            if extension != extension_real:
                self.add_error(
                    "extension",
                    "La extensión indicada no coincide con el archivo.",
                )

        if archivo and tamano_mb is not None:
            tamano_real = Decimal(archivo.size) / Decimal(1024 * 1024)
            if abs(tamano_real - tamano_mb) > Decimal("0.02"):
                self.add_error(
                    "tamano_mb",
                    "El tamaño indicado no coincide con el archivo. "
                    "Consulta su tamaño en MB e inténtalo de nuevo.",
                )

        return datos