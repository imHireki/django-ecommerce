def formata_preco(val=float) -> float:
    return f'R$ {val:.2f}'.replace('.', ',')
    