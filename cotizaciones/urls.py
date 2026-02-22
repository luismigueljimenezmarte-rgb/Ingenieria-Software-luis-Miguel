from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .api import ClienteViewSet, CotizacionViewSet, DetalleCotizacionViewSet

app_name = "cotizaciones"

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'cotizaciones', CotizacionViewSet, basename='cotizacion')
router.register(r'detalles', DetalleCotizacionViewSet, basename='detalle')

urlpatterns = [
    path("", views.cotizacion_list, name="cotizacion_list"),
    path("nueva/", views.cotizacion_create, name="cotizacion_create"),
    path("<int:pk>/", views.cotizacion_detail, name="cotizacion_detail"),
    path("clientes/", views.cliente_list, name="cliente_list"),
    path("clientes/nuevo/", views.cliente_create, name="cliente_create"),
    path("<int:pk>/editar/", views.cotizacion_edit, name="cotizacion_edit"),
    path("<int:pk>/imprimir/", views.cotizacion_print, name="cotizacion_print"),
    path("<int:pk>/pdf/", views.cotizacion_pdf, name="cotizacion_pdf"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("api/", include(router.urls)),
]