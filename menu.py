import os
import time
from validacoes import validar_texto, validar_inteiro, validar_float, formatar_preco, pedir
import repositorio

# Cria a tabela na primeira execução; nas seguintes o IF NOT EXISTS ignora
repositorio.criar_tabela()

while True:
    print(10*'-', "Bem vindo ao Sistema de Gerenciamento de Estoque", 10*'-')
    print("1- Cadastrar Produtos")
    print("2- Listar os Produtos Cadastrados")
    print("3- Atualizar os Produtos")
    print("4- Deletar o produto")
    print("5- Sair do Sistema")

    opcao = input("Digite a opção desejada: ")

    match opcao:

        case '1':
            os.system("cls" if os.name == "nt" else "clear")

            nome_produto = pedir("Digite o nome do produto: ", validar_texto).title()
            quantidade_estoque = pedir("Quantidade de produto em estoque: ", validar_inteiro)
            categoria_produto = pedir("Qual a categoria do produto: ", validar_texto).title()
            preco_produto = pedir("Qual o preço do Produto: ", validar_float)

            # O ID não é informado aqui: quem gera é o AUTOINCREMENT do banco
            repositorio.inserir(nome_produto, categoria_produto, quantidade_estoque, preco_produto)
            print("✅ Produto Cadastrado com Sucesso!")

        case '2':
            os.system("cls" if os.name == "nt" else "clear")
            print("\nLista de Produtos")

            produtos = repositorio.listar()

            if not produtos:
                print("Não há produtos cadastrados!")
            else:
                for p in produtos:
                    print(f"ID: {p['id']}")
                    print(10*'-')
                    print(f"Nome: {p['nome']}")
                    print(10*'-')
                    print(f"Categoria: {p['categoria']}")
                    print(10*'-')
                    print(f"Estoque: {p['estoque']}")
                    print(10*'-')
                    # O banco guarda número puro; formatar_preco só maquia na exibição
                    print(f"Preço: {formatar_preco(p['preco'])}")
                    print(10*'-')

            input("\nPressione ENTER para voltar ao menu inicial...")
            os.system("cls" if os.name == "nt" else "clear")

        case '3':
            os.system("cls" if os.name == "nt" else "clear")

            produtos = repositorio.listar()

            if not produtos:
                print("Nenhum produto cadastrado ainda.")
                input("Pressione ENTER para voltar ao menu...")
                os.system("cls" if os.name == "nt" else "clear")
            else:
                print("Lista de Produtos\n")
                for p in produtos:
                    print(f"ID: {p['id']}")
                    print(10*'-')
                    print(f"Nome: {p['nome']}")
                    print(10*'-')
                    print(f"Categoria: {p['categoria']}")
                    print(10*'-')
                    print(f"Estoque: {p['estoque']}")
                    print(10*'-')
                    print(f"Preço: {formatar_preco(p['preco'])}")
                    print(10*'-')

                procurar_id = pedir("\nDigite o ID do produto que deseja editar: ", validar_inteiro)

                produto_encontrado = repositorio.buscar_por_id(procurar_id)

                if produto_encontrado is None:
                    print("❌ Produto não encontrado")
                else:
                    print(f"\nEditando o Produto: {produto_encontrado['nome']}")
                    print("Deixe em branco e pressione ENTER se não deseja alterar determinado campo.\n")

                    # atual= devolve o valor gravado quando o usuário só aperta ENTER.
                    # Sem ele, o campo seria apagado em vez de mantido.
                    print(f"Nome Atual: {produto_encontrado['nome']}")
                    novo_nome = pedir("Novo Nome (ENTER para manter): ", validar_texto,
                                      atual=produto_encontrado['nome']).title()

                    print(f"\nCategoria Atual: {produto_encontrado['categoria']}")
                    nova_categoria = pedir("Nova Categoria (ENTER para manter): ", validar_texto,
                                           atual=produto_encontrado['categoria']).title()

                    print(f"\nEstoque Atual: {produto_encontrado['estoque']}")
                    novo_estoque = pedir("Novo Estoque (ENTER para manter): ", validar_inteiro,
                                         atual=produto_encontrado['estoque'])

                    print(f"\nPreço Atual: {formatar_preco(produto_encontrado['preco'])}")
                    novo_preco = pedir("Novo Preço (ENTER para manter): ", validar_float,
                                       atual=produto_encontrado['preco'])

                    # Envia os 4 campos mesmo que só um tenha mudado: o UPDATE
                    # do SQL reescreve a linha inteira, não campos avulsos.
                    repositorio.atualizar(procurar_id, novo_nome, nova_categoria,
                                          novo_estoque, novo_preco)
                    print("\n✅ Produto atualizado com sucesso!")

                input("\nPressione ENTER para voltar ao menu...")
                os.system("cls" if os.name == "nt" else "clear")

        case '4':
            os.system("cls" if os.name == "nt" else "clear")

            produtos = repositorio.listar()

            if not produtos:
                print("Nenhum produto cadastrado ainda.")
                input("Pressione ENTER para voltar ao menu...")
                os.system("cls" if os.name == "nt" else "clear")
            else:
                print("Lista de Produtos\n")
                for p in produtos:
                    print(f"ID: {p['id']} | Nome: {p['nome']} | Categoria: {p['categoria']} | "
                          f"Estoque: {p['estoque']} | Preço: {formatar_preco(p['preco'])}")

                procurar_id = pedir("\nDigite o ID do produto que deseja deletar: ", validar_inteiro)

                produto_encontrado = repositorio.buscar_por_id(procurar_id)

                if produto_encontrado is None:
                    print("❌ Produto não encontrado")
                else:
                    # Confirmação antes de deletar para evitar exclusão acidental
                    confirmar = input(f"Tem certeza que deseja deletar '{produto_encontrado['nome']}'? (s/n): ")
                    if confirmar.lower() == 's':
                        repositorio.deletar(procurar_id)
                        print("✅ Produto deletado com sucesso!")
                    else:
                        print("Operação cancelada.")

                input("\nPressione ENTER para voltar ao menu...")
                os.system("cls" if os.name == "nt" else "clear")

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

        case _:
            print("Opção inválida! Tente novamente.")
