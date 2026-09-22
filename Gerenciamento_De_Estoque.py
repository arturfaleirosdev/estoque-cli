import os
import time
import json
from validacoes import validar_texto , validar_inteiro, validar_float, formatar_preco, pedir

ARQUIVO = 'estoque.json'

# Carrega a lista JSON se existir
if os.path.exists(ARQUIVO):
    with open(ARQUIVO, 'r', encoding='utf-8') as arquivo:
        produtos = json.load(arquivo)
else:
    produtos = []

# Define qual ID vai estar disponivel, pegando o seu maximo e somando + 1
if produtos:
    proximo_id = max(p["ID"] for p in produtos) + 1
else:
    proximo_id = 1

while True:
    print(10*'-', "Bem vindo ao Sistema de Gerenciamento de Estoque", 10*'-')
    print("1- Cadastrar Produtos")
    print("2- Listar os Produtos Cadastrados")
    print("3- Atualizar os Produtos")
    print("4- Deletar o produto")
    print("5- Sair do Sistema")

    opcao = input("Digite a opção desejada: ")

    match opcao:

        #  Cadastrar o produto
        case '1':
            os.system("cls" if os.name == "nt" else "clear")

            # Pede os dados do novo produto usando as funções de validação
            nome_produto = pedir("Digite o nome do produto: ").title()
            quantidade_estoque = pedir("Quantidade de produto em estoque: ")
            categoria_produto = validar_texto("Qual a categoria do produto: ").title()
            preco_produto = validar_float("Qual o preço do Produto: ")

            # Monta o dicionário do produto
            produto = {
                "ID": proximo_id,
                "Nome": nome_produto,
                "Categoria": categoria_produto,
                "Estoque": quantidade_estoque,
                "Preço":  preco_produto
            }

            # Adiciona na lista e salva tudo no arquivo JSON
            produtos.append(produto)
            with open(ARQUIVO, 'w', encoding='utf-8') as arquivo:
                json.dump(produtos, arquivo, ensure_ascii=False, indent=4)

            # Atribui o ID após o usuario digitar as informações solicitadas corretamente
            proximo_id += 1
            print("✅ Produto Cadastrado com Sucesso!")

        # Exibir a lista de produtos
        case '2':
            os.system("cls" if os.name == "nt" else "clear")
            print("\nLista de Produtos")

            if not produtos:
                print("Não há produtos cadastrados!")
            else:
                # Percorre a lista e imprime cada produto formatado
                for p in produtos:
                    print(f"ID: {p['ID']}")
                    print(10*'-')
                    print(f"Nome: {p['Nome']}")
                    print(10*'-')
                    print(f"Categoria: {p['Categoria']}")
                    print(10*'-')
                    print(f"Estoque: {p['Estoque']}")
                    print(10*'-')
                    print(f"Preço: {p['Preço']}")
                    print(10*'-')

            input("\nPressione ENTER para voltar ao menu inicial...")
            os.system("cls" if os.name == "nt" else "clear")

        # Atualizar a lista de produtos
        case '3':
            os.system("cls" if os.name == "nt" else "clear")

            if not produtos:
                print("Nenhum produto cadastrado ainda.")
                input("Pressione ENTER para voltar ao menu...")
                os.system("cls" if os.name == "nt" else "clear")
            else:
                # Mostra a lista pra o usuário saber qual ID escolher
                print("Lista de Produtos\n")
                for p in produtos:
                    print(f"ID: {p['ID']}")
                    print(10*'-')
                    print(f"Nome: {p['Nome']}")
                    print(10*'-')
                    print(f"Categoria: {p['Categoria']}")
                    print(10*'-')
                    print(f"Estoque: {p['Estoque']}")
                    print(10*'-')
                    print(f"Preço: {p['Preço']}")
                    print(10*'-')

                # Pede o ID do produto que quer editar (valor() já garante que é número)
                procurar_id = validar_inteiro("\nDigite o ID do produto que deseja editar: ")

                # Procura o produto com esse ID dentro da lista
                produto_encontrado = None
                for p in produtos:
                    if p['ID'] == procurar_id:
                        produto_encontrado = p
                        break
                # Caso o produto não for encontrado no sistema pelo ID
                if produto_encontrado is None:
                    print("❌ Produto não encontrado")
                else:
                    print(f"\nEditando o Produto: {produto_encontrado['Nome']}")
                    print("Deixe em branco e pressione ENTER se não deseja alterar determinado campo.\n")

                    # Mostra o valor atual numa linha, pede o novo valor na linha seguinte
                    print(f"Nome Atual: {produto_encontrado['Nome']}")
                    novo_nome = input("Novo Nome (ENTER para manter): ")
                    
                    if novo_nome.strip():
                        produto_encontrado['Nome'] = novo_nome.title()

                    print(f"\nCategoria Atual: {produto_encontrado['Categoria']}")
                    nova_categoria = input("Nova Categoria (ENTER para manter): ")
                    if nova_categoria.strip():
                        produto_encontrado['Categoria'] = nova_categoria.title()


                    print(f"\nEstoque Atual: {produto_encontrado['Estoque']}")
                    novo_estoque = input("Novo Estoque (ENTER para manter): ")
                    if novo_estoque.strip():
                        produto_encontrado['Estoque'] = int(novo_estoque)

                    print(f"\nPreço Atual: {produto_encontrado['Preço']}")
                    novo_preco = input("Novo Preço (ENTER para manter): ")
                    if novo_preco.strip():
                        produto_encontrado['Preço'] = validar_float(novo_preco)

                    with open(ARQUIVO, 'w', encoding='utf-8') as arquivo:
                        json.dump(produtos, arquivo, ensure_ascii=False, indent=4)

                    print("\n✅ Produto atualizado com sucesso!")

                input("\nPressione ENTER para voltar ao menu...")
                os.system("cls" if os.name == "nt" else "clear")

        # Deletar
        case '4':
            os.system("cls" if os.name == "nt" else "clear")

            if not produtos:
                print("Nenhum produto cadastrado ainda.")
                input("Pressione ENTER para voltar ao menu...")
                os.system("cls" if os.name == "nt" else "clear")
            else:
                print("Lista de Produtos\n")
                for p in produtos:
                    print(f"ID: {p['ID']} | Nome: {p['Nome']} | Categoria: {p['Categoria']} | Estoque: {p['Estoque']} | Preço: {p['Preço']}")

                procurar_id = validar_inteiro("\nDigite o ID do produto que deseja deletar: ")

                produto_encontrado = None
                for p in produtos:
                    if p['ID'] == procurar_id:
                        produto_encontrado = p
                        break

                if produto_encontrado is None:
                    print("❌ Produto não encontrado")
                else:
                    # Confirmação antes de deletar para evitar que o usuario delete sem querer
                    confirmar = input(f"Tem certeza que deseja deletar '{produto_encontrado['Nome']}'? (s/n): ")
                    if confirmar.lower() == 's':
                        produtos.remove(produto_encontrado)
                        with open(ARQUIVO, 'w', encoding='utf-8') as arquivo:
                            json.dump(produtos, arquivo, ensure_ascii=False, indent=4)
                        print("✅ Produto deletado com sucesso!")
                    else:
                        print("Operação cancelada.")

                input("\nPressione ENTER para voltar ao menu...")
                os.system("cls" if os.name == "nt" else "clear")

        # Ultima opção: saída do programa
        case '5':
            print("Saindo do sistema...")
            time.sleep(2)

            total = 20
            for i in range(total + 1):
                porcentagem = (i / total) * 100
                barra = "✅" * i + "-" * (total - i)
                # \r volta o cursor pro início da linha, criando o efeito de barra "andando"
                print(f'\r[{barra}] {porcentagem:.2f}%', end="")
                time.sleep(0.3)

            break
        # Caso o usuario não digite nenhuma opção vale mostra isso
        case _:
            print("Opção inválida! Tente novamente.")