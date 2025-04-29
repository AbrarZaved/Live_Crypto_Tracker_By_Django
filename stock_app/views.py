from django.shortcuts import render

# Create your views here.


def stockPage(request):
    return render(request, "stock_app/stockPage.html")


def stockTracker(request):
    return render(request, "stock_app/stockTracker.html")
