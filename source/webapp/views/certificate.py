from django.shortcuts import render
from webapp.models import Purchase

def verify_certificate(request):
    code = request.GET.get("id")

    context = {}

    try:
        purchase = Purchase.objects.select_related("course", "user").get(payment_code=code, has_certificate=True)
        context["found"] = True
        context["purchase"] = purchase
    except Purchase.DoesNotExist:
        context["found"] = False

    return render(request, "certificate/verify.html", context)