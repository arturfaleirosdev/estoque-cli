# Estoque CLI

Sistema de gerenciamento de estoque em linha de comando, escrito em Python com
persistência em SQLite. Permite cadastrar, consultar, editar e remover produtos,
com validação de entrada e confirmação em operações destrutivas.

Projeto desenvolvido para praticar organização de código em camadas, acesso a
banco de dados relacional e tratamento de erros em Python.

---

## Tecnologias

- **Python 3.10+** (usa `match/case`)
- **SQLite 3** — via `sqlite3`, biblioteca padrão do Python

Sem dependências externas. Não é necessário instalar nada além do Python.

---

## Como rodar

```bash
git clone https://github.com/arturfaleirosdev/estoque-cli
cd estoque-cli
python3 menu.py
```

O banco de dados (`estoque.db`) é criado automaticamente na primeira execução.

---

## Funcionalidades

| Opção | Descrição |
|-------|-----------|
| 1 | Cadastrar produto (nome, quantidade, categoria e preço) |
| 2 | Listar todos os produtos cadastrados |
| 3 | Editar um produto — campos em branco mantêm o valor atual |
| 4 | Remover um produto, com confirmação |
| 5 | Encerrar o programa |

**Validações aplicadas:**

- Nome e categoria não aceitam valores vazios ou puramente numéricos
- Quantidade e preço não aceitam valores negativos
- Preço aceita vírgula ou ponto como separador decimal (`10,50` ou `10.50`)
- Entradas inválidas repetem a pergunta em vez de encerrar o programa

---

## Estrutura do projeto

```
menu.py          Interface de terminal: menus, entrada e exibição
repositorio.py   Acesso ao banco — todo o SQL do projeto está aqui
validacoes.py    Regras de validação e formatação
```

Cada arquivo tem uma responsabilidade única. O `menu.py` nunca escreve SQL, e o
`validacoes.py` nunca imprime nada na tela.

---

## Decisões técnicas

### SQLite em vez de MySQL

O sistema é local e de usuário único, o que não justifica um servidor de banco
de dados. O SQLite já acompanha o Python, então o projeto roda com um único
comando, sem instalação, configuração de usuário ou credenciais.

Como todo o SQL está isolado em `repositorio.py`, migrar para MySQL ou
PostgreSQL exigiria alterar apenas esse arquivo — a interface não mudaria.

### Validação separada da interface

As funções de `validacoes.py` recebem texto e devolvem o valor convertido, ou
levantam `ValueError` com uma mensagem legível. Elas não chamam `input()` nem
`print()`.

Essa separação permite testar as regras sem simular digitação, e reaproveitá-las
em outra interface (web ou API) sem reescrevê-las. A função `pedir()` é a ponte:
ela pergunta, delega a validação e repete em caso de erro.

### Preço armazenado como número

O preço é gravado no banco como valor numérico (`10.5`) e formatado apenas na
exibição (`R$10,50`). Guardar o valor já formatado impediria somas, ordenações e
comparações — e exigiria desfazer a formatação a cada cálculo.

### Consultas parametrizadas

Todas as queries usam marcadores `?` com os valores passados em uma tupla
separada, nunca concatenados na string SQL. Isso impede SQL injection: o valor
é sempre tratado como dado, jamais como comando.

```python
conexao.execute(
    "SELECT * FROM produtos WHERE id = ?", (id_produto,)
)
```

### Restrições no banco

A tabela define `CHECK (estoque >= 0)` e `CHECK (preco >= 0)`. As mesmas regras
já são aplicadas no Python, mas mantê-las também no banco garante a integridade
dos dados mesmo em inserções feitas por fora da aplicação.

O `id` usa `AUTOINCREMENT`, que nunca reutiliza um identificador já emitido —
evitando que um produto novo herde o ID de um produto removido.

---

## Próximos passos

- [ ] Busca de produtos por nome e categoria (`WHERE ... LIKE`)
- [ ] Testes automatizados das regras de validação com `pytest`
- [ ] Relatório de valor total em estoque
- [ ] Listagem em formato de tabela alinhada

---

## Autor

**Artur Faleiros** — [@arturfaleirosdev](https://github.com/arturfaleirosdev)
