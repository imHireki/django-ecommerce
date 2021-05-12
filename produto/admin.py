from django.contrib import admin
from produto.models import Produto, Variacao


class VariacaoInline(admin.TabularInline):
    model = Variacao
    extra = 1

class ProdutoAdmin(admin.ModelAdmin):
    model = Produto
    inlines = [
        VariacaoInline
    ]
    list_display = (
        'nome', 'descricao_curta', 'preco_marketing_f',
        'preco_marketing_promocional_f'
    )


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao, admin.ModelAdmin)
