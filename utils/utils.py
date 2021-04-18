def formata_preco(val):
    return f'R$ {val:.2f}'.replace('.', ',')

def cart_totals(cart):
    return sum([
        item['preco_quantitativo_promocional']
        if item['preco_quantitativo_promocional']
        else item['preco_quantitativo']
        for item in cart.values()
    ]) 

def total_qtd(cart):
    return sum([
        item['quantidade']
        for item
        in cart.values()
    ])