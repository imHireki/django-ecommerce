from math import floor


def valida_cpf(original_cpf) -> bool:
    original_cpf = str(original_cpf)

    # basic validation
    if len(original_cpf) != 11: return False
        
    cpf = original_cpf[:-2]
    reverse_base_cpf = cpf[::-1]
    first_digit = int(original_cpf[-2])
    second_digit = int(original_cpf[-1])

    # sequence validation
    if original_cpf[0]*11 == original_cpf or original_cpf == '01234567890':
        return False
    
    # calcs
    total = 0
    for c, d in enumerate(reverse_base_cpf, 2): total += (c * int(d))
    total_modul_eleven = total % 11

    # rules
    if total_modul_eleven in (1, 0): first_val_d = 0
    if total_modul_eleven in [n for n in range(2, 11)]:
        first_val_d = 11 - total_modul_eleven

    # validation
    if first_val_d != first_digit: return False
        
    # add 10th digit
    cpf_plus_first_d = cpf+str(first_val_d)
    # reverse again 4 the calcs
    reverse_cpf_plus_first_d = cpf_plus_first_d[::-1]

    # calcs
    total_2 = 0
    for c, d in enumerate(reverse_cpf_plus_first_d, 2): total_2 += (c * int(d))
    calc = total_2 - (11 * floor(total_2 / 11))

    # rules
    if calc in (0, 1): second_val_d = 0
    if calc in [n for n in range(2, 11)]: second_val_d = 11 - calc

    # validation
    if second_val_d != second_digit: return False
        
    return True
