from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.http import HttpResponse
from django.conf import settings
import os
from dashboard.models import SiteSettings

def generate_investment_receipt(investment):
    # Get site settings for company info
    site_config = SiteSettings.get_settings()
    
    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{investment.id}.pdf"'

    # Create the PDF object, using the response object as its "file"
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Logo
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
    if os.path.exists(logo_path):
        p.drawImage(logo_path, 0.5 * inch, height - 1.2 * inch, width=1.5 * inch, height=0.5 * inch, preserveAspectRatio=True)

    # Company Info
    p.setFont("Helvetica-Bold", 14)
    p.drawString(2.5 * inch, height - 0.8 * inch, site_config.company_name)
    p.setFont("Helvetica", 10)
    p.drawString(2.5 * inch, height - 1.0 * inch, site_config.company_address)
    p.drawString(2.5 * inch, height - 1.2 * inch, site_config.company_website)

    # Receipt Title
    p.setFont("Helvetica-Bold", 18)
    p.drawString(0.5 * inch, height - 2.5 * inch, "Investment Receipt")
    
    # Investment Details
    p.setFont("Helvetica", 12)
    y = height - 3.2 * inch
    p.drawString(0.5 * inch, y, f"Receipt ID: INV-{investment.id}")
    p.drawString(0.5 * inch, y - 0.3 * inch, f"Date: {investment.start_date.strftime('%Y-%m-%d')}")
    p.drawString(0.5 * inch, y - 0.6 * inch, f"User: {investment.user.email}")
    
    p.drawString(0.5 * inch, y - 1.2 * inch, f"Plan: {investment.plan.name}")
    p.drawString(0.5 * inch, y - 1.5 * inch, f"Amount Invested: ${investment.amount:,.2f}")
    
    # Footer
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(0.5 * inch, 0.5 * inch, f"Thank you for investing with {site_config.company_name}. For support, email {site_config.support_email}")

    p.showPage()
    p.save()
    return response
