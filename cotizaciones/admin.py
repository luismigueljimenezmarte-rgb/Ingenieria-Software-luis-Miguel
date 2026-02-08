from django.contrib import admin
from .models import Cliente, Cotizacion, DetalleCotizacion

class DetalleInline(admin.TabularInline):
    model = DetalleCotizacion
    extra = 1

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    search_fields = ("nombre", "telefono", "correo")

@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "nombre_proyecto", "fecha", "total")
    list_filter = ("fecha",)
    search_fields = ("cliente__nombre", "nombre_proyecto")
    inlines = [DetalleInline]
