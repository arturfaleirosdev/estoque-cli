def valor (mensagem):
    while True:
        try:
            return int(input(mensagem))
        except:
            print("Digite um valor válido!")

def texto (mensagem):
    while True:
        entrada = input(mensagem)
        if entrada.isdigit():
                print("Digite um texto valido!")
        elif not  entrada.strip():
            print("Não há nenhum texto! Digite um texto valido")
        else:
            return entrada
def pedir_float (mensagem):
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Digite um valor válido!")