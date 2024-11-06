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
    if not request.user.purchases.filter(course=course).exists():
        if request.method == 'POST':
            amount = int(course.price * 100)  # цена в тиенах (100 тиен = 1 тенге)
            payment_data = {
                "amount": amount,
                "currency": "KZT",
                "capture_method": "AUTO",
                # "external_id": f"{request.user.id}-{course.id}",
                "description": f"Purchase of {course.title}",
                # "attempts": 10,
                # "success_url": request.build_absolute_uri(reverse('purchase_success')),
                # "failure_url": request.build_absolute_uri(reverse('purchase_failure'))
            }

            headers = {
                'API-KEY': f'{settings.IOKA_SECRET_KEY}',
                'Content-Type': 'application/json'
            }

            response = requests.post('https://stage-api.ioka.kz/v2/orders', json=payment_data, headers=headers)
            logger.info("STATUS", response.status_code)
            if response.status_code == 201:
                payment = response.json()
                return redirect(payment['order']['checkout_url'])
            else:
                error_data = response.json()
                logger.error('API ERROR', error_data)
                return render(request, 'purchase/purchase_failure.html', {'error': response.json()})
        else:
            return render(request, 'purchase/purchase_course.html', {'course': course})
    return redirect('course_detail', pk=course_id)

@login_required
def purchase_success(request):
    # Обработка успешного платежа
    order_id = request.GET.get('order_id')
    user_id, course_id = order_id.split('-')
    user = get_object_or_404(settings.AUTH_USER_MODEL, id=user_id)
    course = get_object_or_404(Course, id=course_id)
    if not user.purchases.filter(course=course).exists():
        Purchase.objects.create(user=user, course=course, payment_status='PAID')
    return redirect('course_detail', pk=course_id)

@login_required
def purchase_failure(request):
    # Обработка неуспешного платежа
    return render(request, 'purchase/purchase_failure.html')
