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

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from datetime import datetime
import os
from django.conf import settings


def generate_certificate(purchase):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.colors import HexColor
    from datetime import datetime

    # Пути
    font_dir = settings.STATICFILES_DIRS[0]
    logo_path = os.path.join(font_dir, 'img', 'SkillSpring1.png')
    seal_path = os.path.join(font_dir, 'new_img', 'img.png')
    print(f"[DEBUG] Путь до печати: {seal_path}")
    print(f"[DEBUG] Печать доступна: {os.access(seal_path, os.R_OK)}")
    print(seal_path)
    regular_font = os.path.join(font_dir, 'fonts', 'Roboto-Regular.ttf')
    bold_font = os.path.join(font_dir, 'fonts', 'Roboto-Bold.ttf')

    pdfmetrics.registerFont(TTFont("Roboto", regular_font))
    pdfmetrics.registerFont(TTFont("Roboto-Bold", bold_font))

    filename = f"certificate_{purchase.user.username}_{purchase.course.id}.pdf"
    relative_path = f'certificates/{filename}'
    filepath = os.path.join(settings.MEDIA_ROOT, relative_path)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Цвета
    green = HexColor("#30BC83")
    gray = HexColor("#f2f2f2")
    black = HexColor("#000000")
    dark_gray = HexColor("#444444")

    width, height = A4
    c = canvas.Canvas(filepath, pagesize=A4)

    # Фон
    c.setFillColor(gray)
    c.rect(0, 0, width, height, fill=1)

    # Белый блок по центру
    margin = 50
    c.setFillColor("white")
    c.rect(margin, margin, width - 2 * margin, height - 2 * margin, fill=1)

    # Логотип
    if os.path.exists(logo_path):
        c.drawImage(logo_path, width / 2 - 75, height - 160, width=150, preserveAspectRatio=True, mask='auto')

    # Заголовок
    c.setFont("Roboto-Bold", 26)
    c.setFillColor(black)
    c.drawCentredString(width / 2, height - 200, "CERTIFICATE OF COMPLETION")

    # Имя
    user_name = purchase.user.get_full_name() or purchase.user.username
    c.setFont("Roboto-Bold", 20)
    c.drawCentredString(width / 2, height - 260, user_name)

    # Подпись
    c.setFont("Roboto", 13)
    c.setFillColor(dark_gray)
    c.drawCentredString(width / 2, height - 285, "has successfully completed the course")

    # Название курса
    c.setFont("Roboto-Bold", 16)
    c.setFillColor(green)
    c.drawCentredString(width / 2, height - 310, purchase.course.title)

    # Подстрочный текст
    c.setFont("Roboto", 10)
    c.setFillColor(dark_gray)
    c.drawCentredString(width / 2, height - 330, "An online non-credit course authorized by SkillSpring")

    # Дата
    date_str = datetime.today().strftime("%B %d, %Y")
    c.setFont("Roboto", 10)
    c.drawCentredString(width / 2, height - 370, date_str)

    # Полупрозрачная надпись
    c.setFont("Roboto-Bold", 60)
    c.setFillColor(HexColor("#eeeeee"))
    c.drawCentredString(width / 2, height / 2 + 30, "SKILLSPRING")

    # Рамка
    c.setStrokeColor(green)
    c.setLineWidth(4)
    c.rect(margin, margin, width - 2 * margin, height - 2 * margin, stroke=1, fill=0)

    # Линия под заголовком
    c.setStrokeColor(green)
    c.setLineWidth(1)
    c.line(width / 2 - 100, height - 210, width / 2 + 100, height - 210)

    # Печать внизу, аккуратно под текстом
    if os.path.exists(seal_path):
        seal_image = ImageReader(seal_path)
        c.drawImage(seal_image, width / 2 - 50, margin + 160, width=100, preserveAspectRatio=True, mask='auto')

    # Подпись CEO
    c.setFont("Roboto", 10)
    c.drawString(margin + 20, margin + 80, "_________________________")
    c.drawString(margin + 20, margin + 65, "Uldana Moldabayeva")
    c.drawString(margin + 20, margin + 52, "CEO, SkillSpring")

    # Футер
    c.setFont("Roboto", 9)
    c.setFillColor(dark_gray)
    c.drawCentredString(width / 2, margin + 25, "SkillSpring · skillspring.io")

    c.showPage()
    c.save()

    # Возврат относительного пути
    return relative_path