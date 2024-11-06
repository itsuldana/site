from django.views.generic import TemplateView
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.conf import settings
from ..forms import ContactForm

import logging

logger = logging.getLogger(__name__)

class HelpView(TemplateView):
    template_name = "help.html"


def send_email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            # Извлекаем данные из формы
            name = form.cleaned_data.get('name', 'No Name Provided')
            last_name = form.cleaned_data.get('last_name', 'No Last Name Provided')
            email = form.cleaned_data.get('email', 'No Email Provided')
            phone = form.cleaned_data.get('phone', 'No Phone Provided')
            message = form.cleaned_data.get('message', 'No Message Provided')
            attach_file = form.cleaned_data.get('attach_file')

            # Формируем email
            email_subject = f'Contacting support: '
            email_body = f"Name: {name}\nLast Name: {last_name}\nEmail: {email}\nPhone: {phone}\nMessage:\n{message}\n\n"
            email_message = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['glebtgd@gmail.com'],  # замените на ваш email
            )

            # Прикрепляем файл, если он есть
            if attach_file:
                email_message.attach(attach_file.name, attach_file.read(), attach_file.content_type)

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
    return render(request, 'help.html', {'form': form})
