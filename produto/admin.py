from django.contrib import admin
from produto.models import Produto


class ProdutoAdmin(admin.ModelAdmin):
    model = Produto


admin.site.register(Produto, ProdutoAdmin)
