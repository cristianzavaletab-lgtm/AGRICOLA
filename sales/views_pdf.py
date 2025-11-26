import os
from urllib.parse import quote
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .models import Sale

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError):
    WEASYPRINT_AVAILABLE = False

@login_required
def invoice_pdf(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    html_string = render_to_string('sales/invoice_pdf.html', {'sale': sale})

    if WEASYPRINT_AVAILABLE:
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="boleta_{sale.id}.pdf"'
        response.write(result)
        return response

    # Fallback: guardar HTML del comprobante y ofrecer compartir por WhatsApp
    invoices_dir = os.path.join(settings.MEDIA_ROOT, 'invoices')
    os.makedirs(invoices_dir, exist_ok=True)
    file_name = f'boleta_{sale.id}.html'
    file_path = os.path.join(invoices_dir, file_name)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_string)

    public_url = request.build_absolute_uri(f"{settings.MEDIA_URL}invoices/{file_name}")

    whatsapp_text = quote(f"Comprobante de venta #{sale.id} - Total S/ {sale.total}\n{public_url}")
    whatsapp_url = f"https://wa.me/?text={whatsapp_text}"

    page_html = render_to_string('sales/invoice_share.html', {
        'sale': sale,
        'public_url': public_url,
        'whatsapp_url': whatsapp_url,
    })

    return HttpResponse(page_html)
