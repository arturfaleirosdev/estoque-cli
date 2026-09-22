"""Regras de validação e formatação.

Estas funções não imprimem nem perguntam nada de propósito: elas recebem
texto e devolvem o valor convertido, ou levantam ValueError explicando o
problema. Manter a regra separada da interface permite testá-la sem
terminal e reaproveitá-la em outra interface (web, API) no futuro.

A única exceção é `pedir`, que é a ponte entre as duas coisas.
"""

def validar_inteiro (entrada: str, minimo: int= 0):
    try:
        numero = int(entrada)
    except ValueError:
        raise ValueError("Digite um número inteiro válido!")
    if numero < minimo:
        raise ValueError(f"O valor precisa ser maior ou igual a {minimo}!")
    return numero
    

def validar_float (entrada: str, minimo: float = 0.0):
    entrada =  entrada.strip().replace(',', '.')
    try:
        numero = float(entrada)
    except ValueError:
        raise ValueError("Digite um número válido!")
    if numero < minimo:
        raise ValueError(f"O valor precisa ser maior ou igual a {minimo}!")
    return numero

def validar_texto(entrada: str):
    entrada = entrada.strip()
    if not entrada:
        raise ValueError("Não há nenhum texto! Digite um texto válido.")
    if entrada.isdigit():
        raise ValueError("Digite um texto válido!")
    return entrada

def formatar_preco(preco: float):
    return f"R${preco:.2f}".replace('.',',')

def pedir(mensagem, validador, atual=None):
    while True:
        bruto = input(mensagem)

        if atual is not None and not bruto.strip():
            return atual

        try:
            return validador(bruto)
        except ValueError as erro:
            print(erro)
