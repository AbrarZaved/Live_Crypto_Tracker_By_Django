from django.urls import path, include

from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.stockPage, name="stockPage"),
    path("stockTracker/", views.stockTracker, name="stockTracker"),
]
