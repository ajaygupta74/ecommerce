from datetime import datetime, timezone
import qrcode
from io import BytesIO
from django.conf import settings


def generate_qr_code(order):
    UPI_ID = settings.PAYMENT_UPI_ID
    BUSINESS_TITLE = 'Growsmo'
    ORDER_TITLE = f"Payment for order - {order.slug}"
    ORDER_MESSAGE = f"{order.pk} by {order.user}"
    COUNTRY_CODE = "INR"
    url = (f"upi://pay?pa={UPI_ID}&pn={BUSINESS_TITLE}&tn={ORDER_TITLE}"
           f"&am={float(order.order_price)}&cu={COUNTRY_CODE}"
           f"&mc={ORDER_MESSAGE}")
    print(url)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    filename = f"order_qrcode_{order.pk}_{current_time}.png"
    order.qr_code.save(filename, img_buffer)
    order.save(update_fields=['qr_code'])
