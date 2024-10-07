from django.shortcuts import render


def test_main_page(request):
    return render(request, 'main.html')
