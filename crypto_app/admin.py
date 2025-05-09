from django.contrib import admin

from crypto_app.models import Crypto

# Register your models here.

@admin.register(Crypto)
class CryptoAdmin(admin.ModelAdmin):
    list_display = ("symbol",)
    search_fields = ("symbol",)
    list_filter = ("user",)
    ordering = ("symbol",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("user")