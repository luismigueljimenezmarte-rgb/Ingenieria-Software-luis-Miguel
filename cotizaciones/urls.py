from django.urls import path
from . import views

app_name = "cotizaciones"

urlpatterns = [
    path("", views.cotizacion_list, name="cotizacion_list"),
    path("nueva/", views.cotizacion_create, name="cotizacion_create"),
    path("<int:pk>/", views.cotizacion_detail, name="cotizacion_detail"),
    path("clientes/", views.cliente_list, name="cliente_list"),
    path("clientes/nuevo/", views.cliente_create, name="cliente_create"),
    path("<int:pk>/editar/", views.cotizacion_edit, name="cotizacion_edit"),
    path("<int:pk>/imprimir/", views.cotizacion_print, name="cotizacion_print"),
    path("<int:pk>/pdf/", views.cotizacion_pdf, name="cotizacion_pdf"),

]
