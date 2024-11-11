from django.views.generic import TemplateView
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.conf import settings
from ..forms import ContactForm

import logging

logger = logging.getLogger(__name__)


class ContactUsView(TemplateView):
    template_name = "contact_us.html"


def send_email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Извлекаем данные из формы
            name = form.cleaned_data.get('name', 'No Name Provided')
            email = form.cleaned_data.get('email', 'No Email Provided')
            number = form.cleaned_data.get('number', 'No Phone Provided')
            message = form.cleaned_data.get('message', 'No Message Provided')

            # Формируем email
            email_subject = f'Contacting support: '
            email_body = f"Name: {name}\nEmail: {email}\nPhone: {number}\nMessage:\n{message}\n\n"
            email_message = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['glebtgd@gmail.com'],  # замените на ваш email
            )

            # Логирование перед отправкой
            logger.info(f"Attempting to send email with subject: {email_subject} and body: {email_body}")

            try:
                email_message.send()
                logger.info("Email sent successfully.")
                return render(request, 'success.html')  # Перенаправляем на страницу успеха
            except Exception as e:
                logger.error(f"Failed to send email: {e}")
                return render(request, 'error.html')  # Рендерим страницу ошибки

    # Если запрос не POST или форма невалидна, просто рендерим форму
    else:
        form = ContactForm()
    return render(request, 'contact_us.html', {'form': form})
