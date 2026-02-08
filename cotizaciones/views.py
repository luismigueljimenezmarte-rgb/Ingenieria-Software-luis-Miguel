from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import Cliente, Cotizacion
from .forms import ClienteForm, CotizacionForm, DetalleFormSet
from django.http import HttpResponse
from decimal import Decimal



def cotizacion_list(request):
    cotizaciones = Cotizacion.objects.select_related("cliente").order_by("-id")
    return render(request, "cotizaciones/cotizacion_list.html", {"cotizaciones": cotizaciones})


@transaction.atomic
def cotizacion_create(request):
    if request.method == "POST":
        form = CotizacionForm(request.POST)
        if form.is_valid():
            cotizacion = form.save()
            formset = DetalleFormSet(request.POST, instance=cotizacion)
            if formset.is_valid():
                formset.save()
                cotizacion.recalcular_total()
                return redirect("cotizaciones:cotizacion_detail", pk=cotizacion.pk)
    else:
        form = CotizacionForm()
        formset = DetalleFormSet()

    return render(request, "cotizaciones/cotizacion_create.html", {"form": form, "formset": formset})


def cotizacion_detail(request, pk):
    cotizacion = get_object_or_404(Cotizacion.objects.select_related("cliente"), pk=pk)
    detalles = cotizacion.detalles.all().order_by("id")
    return render(request, "cotizaciones/cotizacion_detail.html", {"cotizacion": cotizacion, "detalles": detalles})


def cliente_list(request):
    clientes = Cliente.objects.order_by("nombre")
    return render(request, "cotizaciones/cliente_list.html", {"clientes": clientes})


def cliente_create(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cotizaciones:cliente_list")
    else:
        form = ClienteForm()
    return render(request, "cotizaciones/cliente_form.html", {"form": form})



@transaction.atomic
def cotizacion_edit(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)

    if request.method == "POST":
        form = CotizacionForm(request.POST, instance=cotizacion)
        formset = DetalleFormSet(request.POST, instance=cotizacion)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            cotizacion.recalcular_total()
            return redirect("cotizaciones:cotizacion_detail", pk=cotizacion.pk)
    else:
        form = CotizacionForm(instance=cotizacion)
        formset = DetalleFormSet(instance=cotizacion)

    return render(
        request,
        "cotizaciones/cotizacion_edit.html",
        {"form": form, "formset": formset, "cotizacion": cotizacion},
    )

def cotizacion_print(request, pk):
    cotizacion = get_object_or_404(Cotizacion.objects.select_related("cliente"), pk=pk)
    detalles = cotizacion.detalles.all().order_by("id")
    return render(
        request,
        "cotizaciones/cotizacion_print.html",
        {"cotizacion": cotizacion, "detalles": detalles},
    )


def cotizacion_pdf(request, pk):
    # PDF con ReportLab (no depende de weasyprint)
    from io import BytesIO
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    cotizacion = get_object_or_404(Cotizacion.objects.select_related("cliente"), pk=pk)
    detalles = cotizacion.detalles.all().order_by("id")

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"Cotización #{cotizacion.id}")
    y -= 25

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Cliente: {cotizacion.cliente.nombre}")
    y -= 14
    c.drawString(50, y, f"Tel: {cotizacion.cliente.telefono}  |  Correo: {cotizacion.cliente.correo}")
    y -= 14
    c.drawString(50, y, f"Dirección: {cotizacion.cliente.direccion}")
    y -= 18

    c.drawString(50, y, f"Proyecto: {cotizacion.nombre_proyecto}")
    y -= 14
    c.drawString(50, y, f"Tipo de obra: {cotizacion.tipo_obra}  |  Ubicación: {cotizacion.ubicacion}")
    y -= 14
    c.drawString(50, y, f"Fecha: {cotizacion.fecha}")
    y -= 22

    # Encabezados tabla
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Descripción")
    c.drawString(260, y, "Cat.")
    c.drawString(320, y, "Unidad")
    c.drawRightString(400, y, "Cant.")
    c.drawRightString(480, y, "Precio")
    c.drawRightString(560, y, "Subtotal")
    y -= 12
    c.line(50, y, 560, y)
    y -= 14

    c.setFont("Helvetica", 9)
    total = Decimal("0.00")

    def rd(n):
        try:
            return f"RD$ {float(n):,.2f}"
        except Exception:
            return str(n)

    for d in detalles:
        # salto de página si no cabe
        if y < 80:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, y, "Descripción")
            c.drawString(260, y, "Cat.")
            c.drawString(320, y, "Unidad")
            c.drawRightString(400, y, "Cant.")
            c.drawRightString(480, y, "Precio")
            c.drawRightString(560, y, "Subtotal")
            y -= 12
            c.line(50, y, 560, y)
            y -= 14
            c.setFont("Helvetica", 9)

        desc = (d.descripcion or "")[:36]
        c.drawString(50, y, desc)
        c.drawString(260, y, (d.get_categoria_display() or "")[:10])
        c.drawString(320, y, (d.get_unidad_pago_display() or "")[:10])
        c.drawRightString(400, y, str(d.cantidad))
        c.drawRightString(480, y, rd(d.precio_unitario))
        c.drawRightString(560, y, rd(d.subtotal))
        total += (d.subtotal or Decimal("0.00"))
        y -= 14

    y -= 10
    c.setFont("Helvetica-Bold", 11)
    c.line(350, y, 560, y)
    y -= 18
    c.drawRightString(560, y, f"TOTAL: {rd(total)}")

    c.showPage()
    c.save()

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="cotizacion_{cotizacion.id}.pdf"'
    response.write(pdf)
    return response

