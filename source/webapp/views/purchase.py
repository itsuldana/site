import random
from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
from rest_framework.generics import get_object_or_404

from webapp.models import Purchase, Course


class PurchaseCreateView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        # Генерация случайного шестнадцатеричного числа (6 символов)
        payment_code = f'{random.randint(0, 0xFFFFFF):06X}'

        # Считаем стоимость заказа
        # Получаем скидку пользователя в процентах
        user_discount = request.user.get_user_discount()  # Например, 20 для 20%

        # Считаем стоимость заказа с учетом скидки
        discounted_price = course.price * (Decimal(100 - user_discount) / Decimal(100))

        # Округляем до целого числа
        purchase_amount = discounted_price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

        # Создание заказа со статусом PENDING
        purchase = Purchase.objects.create(
            user=request.user,
            course=course,
            payment_status='PENDING',
            payment_code=payment_code,
            purchase_amount=purchase_amount,
        )

        # Редирект на страницу с инструкцией
        return redirect(reverse('payment_qr', kwargs={'pk': purchase.pk}))


class PaymentQRView(DetailView):
    template_name = 'purchase/purchase_qr.html'

    model = Purchase
    context_object_name = 'purchase'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['course'] = get_object_or_404(Course, id=self.object.course_id)

        context['purchase_amount'] = self.object.purchase_amount

        context['discount'] = self.request.user.get_user_discount()

        return context