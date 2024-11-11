# webapp/views/purchase.py

import requests
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from webapp.models import Course
from webapp.models.purchase import Purchase
import logging

logger = logging.getLogger(__name__)


@login_required
def purchase_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        purchase = Purchase.objects.create(user=request.user, course=course)
        amount = int(course.price * 100)  # цена в тиенах (100 тиен = 1 тенге)
        success_url = request.build_absolute_uri(reverse('purchase_success'))
        failure_url = request.build_absolute_uri(reverse('purchase_failure'))
        logger.error(f'Success URL: {success_url}')
        logger.error(f'Failure URL: {failure_url}')
        payment_data = {
            "amount": amount,
            "currency": "KZT",
            "capture_method": "AUTO",
            "external_id": f"{purchase.id}",
            "description": f"Purchase of {course.title}",
            "attempts": 10,
            "success_url": f'{success_url}',
            "failure_url": f'{failure_url}'
        }

        headers = {
            'API-KEY': f'{settings.IOKA_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        response = requests.post('https://stage-api.ioka.kz/v2/orders', json=payment_data, headers=headers)

        logger.error(f'STATUS {response.json()}')
        if response.status_code == 201:
            payment = response.json()
            return redirect(payment['order']['checkout_url'] + "?autoRedirectMs=5000")
        else:
            error_data = response.json()
            logger.error('API ERROR', error_data)
            return render(request, 'purchase/purchase_failure.html', {'error': response.json()})

    return redirect('course_detail', pk=course_id)


@login_required
def purchase_success(request):
    # Обработка успешного платежа
    order_id = request.GET.get('external_id')

    if not order_id:
        logger.error("Не передан order_id")
        return redirect('purchase_failure')

    try:
        purchase = Purchase.objects.get(id=order_id)
        purchase.payment_status = 'PAID'
        purchase.save()
    except Purchase.DoesNotExist:
        logger.error(f"Purchase с id={order_id} не найден")
        return redirect('purchase_failure')

    return redirect('course_detail', pk=purchase.course.id)


@login_required
def purchase_failure(request):
    order_id = request.GET.get('external_id')
    if not order_id:
        logger.error("Не передан order_id")
        return redirect('some_error_page')  # Редирект в случае отсутствия order_id

    try:
        purchase = Purchase.objects.get(id=order_id)

        purchase.delete()
        logger.info(f"Запись Purchase с id={order_id} успешно удалена после неудачной оплаты")

    except Purchase.DoesNotExist:
        logger.error(f"Запись Purchase с id={order_id} не найдена для удаления")

    return redirect(request, 'purchase/purchase_failure.html')
