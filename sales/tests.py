from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.conf import settings
from .models import Sale
from . import views_pdf

class InvoicePublicUrlTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='tester', password='pass')

    def test_public_url_uses_app_base_url(self):
        settings.APP_BASE_URL = 'https://agro-inversiones-pos.onrender.com'
        views_pdf.WEASYPRINT_AVAILABLE = False
        sale = Sale.objects.create(total=40)
        request = self.factory.get(f'/sales/invoice/{sale.id}/pdf/')
        request.user = self.user
        response = views_pdf.invoice_pdf(request, sale.id)
        self.assertEqual(response.status_code, 200)
        expected = f'https://agro-inversiones-pos.onrender.com{settings.MEDIA_URL}invoices/boleta_{sale.id}.html'
        self.assertIn(expected, response.content.decode('utf-8'))
