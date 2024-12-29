
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import re

def sanitize_filename(filename):
    """Remove invalid characters from the filename."""
    return re.sub(r'[\\/:"*?<>|]+', '_', filename)

class QrGenerator(models.Model):
    name = models.CharField(max_length=255)
    qr_code = models.ImageField(default='qr_code.png', null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Generate the QR code
        qrcode_img = qrcode.make(self.name)

        # Ensure the QR code image fits the canvas size
        qrcode_img = qrcode_img.resize((290, 290))  # Resize QR code to fit within the canvas

        canvas = Image.new('RGB', (290, 290), 'white')  # Create a white canvas
        position = ((canvas.width - qrcode_img.width) // 2,  # Center horizontally
                    (canvas.height - qrcode_img.height) // 2)  # Center vertically

        canvas.paste(qrcode_img, position)  # Paste the resized QR code onto the canvas

        # Sanitize the filename
        safe_name = sanitize_filename(self.name)
        fname = f'qr_code-{safe_name}.png'

        # Create an in-memory file object
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        buffer.seek(0)

        # Save the QR code image to the ImageField
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()

        # Call the parent save method
        super().save(*args, **kwargs)
