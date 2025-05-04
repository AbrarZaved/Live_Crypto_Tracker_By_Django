from django.urls import path, include

from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.crypto_home, name="crypto_home"),
    path("crypto_quotes/", views.crypto_quotes, name="crypto_quotes"),
]
