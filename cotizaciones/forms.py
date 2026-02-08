from django import forms
from django.forms import inlineformset_factory
from .models import Cliente, Cotizacion, DetalleCotizacion


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "telefono", "correo", "direccion"]


class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ["cliente", "nombre_proyecto", "tipo_obra", "ubicacion", "fecha", "notas"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "notas": forms.Textarea(attrs={"rows": 3}),
        }


class DetalleCotizacionForm(forms.ModelForm):
    class Meta:
        model = DetalleCotizacion
        fields = ["descripcion", "categoria", "unidad_pago", "cantidad", "precio_unitario"]

    def clean(self):
        cleaned = super().clean()
        desc = (cleaned.get("descripcion") or "").strip()

        # Si está vacía, la dejamos pasar como vacía (no obliga)
        if desc == "":
            # Marcamos el formulario como vacío: limpiamos errores de campos requeridos
            # (Django ya suele ignorar empty_permitted en extras, pero esto ayuda)
            cleaned["cantidad"] = cleaned.get("cantidad") or 0
            cleaned["precio_unitario"] = cleaned.get("precio_unitario") or 0

        return cleaned


DetalleFormSet = inlineformset_factory(
    Cotizacion,
    DetalleCotizacion,
    form=DetalleCotizacionForm,
    extra=10,             # pon 10 o más si quieres
    can_delete=True,
)
