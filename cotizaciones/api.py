from rest_framework import serializers, viewsets
from .models import Cliente, Cotizacion, DetalleCotizacion


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"


class DetalleCotizacionSerializer(serializers.ModelSerializer):
    categoria_display = serializers.CharField(source="get_categoria_display", read_only=True)
    unidad_display = serializers.CharField(source="get_unidad_pago_display", read_only=True)

    class Meta:
        model = DetalleCotizacion
        fields = "__all__"


class CotizacionSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source="cliente.nombre", read_only=True)
    detalles = DetalleCotizacionSerializer(many=True, read_only=True)

    class Meta:
        model = Cotizacion
        fields = "__all__"


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by("-id")
    serializer_class = ClienteSerializer


class CotizacionViewSet(viewsets.ModelViewSet):
    queryset = Cotizacion.objects.select_related("cliente").all().order_by("-id")
    serializer_class = CotizacionSerializer


class DetalleCotizacionViewSet(viewsets.ModelViewSet):
    queryset = DetalleCotizacion.objects.select_related("cotizacion").all().order_by("-id")
    serializer_class = DetalleCotizacionSerializer