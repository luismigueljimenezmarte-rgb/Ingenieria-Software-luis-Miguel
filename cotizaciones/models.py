from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    telefono = models.CharField(max_length=30, blank=True)
    correo = models.EmailField(blank=True)
    direccion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nombre


class Cotizacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="cotizaciones")
    nombre_proyecto = models.CharField(max_length=150)
    tipo_obra = models.CharField(max_length=80, blank=True)
    ubicacion = models.CharField(max_length=150, blank=True)
    fecha = models.DateField(default=timezone.now)
    notas = models.TextField(blank=True)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return f"Cotización #{self.id} - {self.cliente.nombre}"

    def recalcular_total(self):
        total = sum([d.subtotal for d in self.detalles.all()])
        self.total = total
        self.save(update_fields=["total"])


class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name="detalles")
    descripcion = models.CharField(max_length=200)
    categoria = models.CharField(
        max_length=30,
        choices=[("MATERIAL", "Material"), ("MANO_OBRA", "Mano de obra"), ("OTRO", "Otro")],
        default="MATERIAL",
    )

    unidad_pago = models.CharField(
        max_length=20,
        choices=[
            ("HORA", "Hora"),
            ("DIA", "Día"),
            ("SEMANA", "Semana"),
            ("MES", "Mes"),
            ("SERVICIO", "Servicio"),
            ("M2", "m²"),
            ("ML", "Metro lineal"),
            ("VIAJE", "Viaje"),
            ("UNIDAD", "Unidad"),
        ],
        default="DIA",
    )

    cantidad = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = (self.cantidad or 0) * (self.precio_unitario or 0)
        super().save(*args, **kwargs)
