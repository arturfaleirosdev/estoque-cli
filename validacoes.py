
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

def pedir(mensagem, validador):
    while True:
        try:
            return validador(input(mensagem))
        except ValueError as erro:
            print(erro)

