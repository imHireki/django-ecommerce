def get_qtd_total(carrinho):
    qtd_total = sum([
        item['quantidade']
        for item in carrinho.values()
    ])
    return qtd_total

def formata_preco(val=float) -> float:
    return f'R$ {val:.2f}'.replace('.', ',')

def get_total(carrinho) -> str:
    total = sum([
        item['preco_quantitativo_promocional']
        if item['preco_quantitativo_promocional']
        else item['preco_quantitativo']
        for item in carrinho.values()
    ])

    return total