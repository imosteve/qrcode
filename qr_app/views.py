
from django.shortcuts import render
from .models import QrGenerator
from django.conf import settings
import os

def generate_qr(request):
    qr = None  # Default QR code (blank initially)
    
    if request.method == 'POST':
        link = request.POST.get('link')

        if not link:
            qr_placeholder = os.path.join(settings.MEDIA_URL, 'qr_code.png')
            return render(request, 'qr_app/qr_form.html', {'error': 'Link is required', 'qr': qr_placeholder})
        
        # Create and save the QR code
        qr = QrGenerator.objects.create(name=link)
        # qr.save()

    # If no QR is generated, use a blank placeholder image
    if not qr:
        qr_placeholder = os.path.join(settings.MEDIA_URL, 'qr_code.png')
        return render(request, 'qr_app/qr_form.html', {'qr': qr_placeholder})

    # Render the page with the generated QR code
    return render(request, 'qr_app/qr_form.html', {'qr': qr.qr_code.url})
