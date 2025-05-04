from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
import os

# Регистрация шрифта Roboto (нужен .ttf файл!)
font_dir = settings.STATICFILES_DIRS[0]

pdfmetrics.registerFont(TTFont('Roboto', os.path.join(font_dir, 'fonts', 'Roboto-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Roboto-Bold', os.path.join(font_dir, 'fonts', 'Roboto-Bold.ttf')))


def generate_certificate(purchase):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.colors import HexColor
    from reportlab.lib.utils import ImageReader
    from reportlab.lib.units import mm
    from datetime import datetime
    import os
    import qrcode

    # Пути
    font_dir = settings.STATICFILES_DIRS[0]
    logo_path = os.path.join(font_dir, 'img', 'SkillSpring1.png')
    seal_path = os.path.join(font_dir, 'new_img', 'img.png')
    pattern_path = os.path.join(settings.BASE_DIR, 'static', 'new_img', 'certificate-background.jpg')
    print(f"[DEBUG] pattern_path: {pattern_path}, exists: {os.path.exists(pattern_path)}")
    regular_font = os.path.join(font_dir, 'fonts', 'Roboto-Regular.ttf')
    bold_font = os.path.join(font_dir, 'fonts', 'Roboto-Bold.ttf')

    # Регистрация шрифтов
    pdfmetrics.registerFont(TTFont("Roboto", regular_font))
    pdfmetrics.registerFont(TTFont("Roboto-Bold", bold_font))

    # Название файла
    filename = f"certificate_{purchase.user.username}_{purchase.course.id}.pdf"
    relative_path = f'certificates/{filename}'
    filepath = os.path.join(settings.MEDIA_ROOT, relative_path)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # QR-код
    qr_url = f"https://skillspring.oyustudio.kz/certificate/verify?id={purchase.payment_code}"
    qr_path = os.path.join(settings.MEDIA_ROOT, 'certificates', f"qr_{purchase.id}.png")
    qrcode.make(qr_url).save(qr_path)

    # Цвета
    green = HexColor("#30BC83")
    black = HexColor("#000000")
    dark_gray = HexColor("#444444")

    width, height = A4
    margin = 50
    c = canvas.Canvas(filepath, pagesize=A4)

    # Фон
    c.setFillColor("white")
    c.rect(0, 0, width, height, fill=1)
    if os.path.exists(pattern_path):
        c.drawImage(pattern_path, 0, 0, width=width, height=height, mask='auto')

    # Заголовок
    c.setFont("Roboto-Bold", 26)
    c.setFillColor(black)
    c.drawCentredString(width / 2, height - 160, "CERTIFICATE OF COMPLETION")
    c.setStrokeColor(green)
    c.setLineWidth(1)
    c.line(width / 2 - 100, height - 170, width / 2 + 100, height - 170)

    # Имя пользователя
    name = purchase.user.get_full_name() or purchase.user.username
    c.setFont("Roboto-Bold", 20)
    c.drawCentredString(width / 2, height - 220, name)

    # Основной текст
    c.setFont("Roboto", 13)
    c.setFillColor(dark_gray)
    c.drawCentredString(width / 2, height - 245, "has successfully completed the course")

    # Название курса
    c.setFont("Roboto-Bold", 16)
    c.setFillColor(green)
    c.drawCentredString(width / 2, height - 270, purchase.course.title)

    # Подстрочный текст
    c.setFont("Roboto", 10)
    c.setFillColor(dark_gray)
    c.drawCentredString(width / 2, height - 290, "An online non-credit course authorized by SkillSpring")

    # Печать под текстом
    if os.path.exists(seal_path):
        c.drawImage(seal_path, width / 2 - 40, height - 340, width=80, preserveAspectRatio=True, mask='auto')

    # Дата
    c.setFont("Roboto", 10)
    c.setFillColor(dark_gray)
    c.drawCentredString(width / 2, margin + 120, datetime.today().strftime("%B %d, %Y"))

    # Подпись CEO
    c.setFont("Roboto", 10)
    c.setFillColor(black)
    c.drawString(margin + 20, margin + 70, "_________________________")
    c.drawString(margin + 20, margin + 55, "Uldana Moldabayeva")
    c.drawString(margin + 20, margin + 42, "CEO, SkillSpring")

    # QR-код
    if os.path.exists(qr_path):
        c.drawImage(qr_path, width - margin - 35 * mm, margin + 25, width=30 * mm, height=30 * mm)

    # Футер
    c.setFont("Roboto", 9)
    c.setFillColor(dark_gray)
    c.drawCentredString(width / 2, margin + 20, "SkillSpring · skillspring.io")

    c.showPage()
    c.save()

    # Сохраняем путь в модель
    if hasattr(purchase, "certificate_file"):
        purchase.certificate_file = relative_path
        purchase.save(update_fields=["certificate_file"])

    return relative_path