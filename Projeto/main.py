import sys

import firebase_admin
from firebase_admin import credentials, firestore

from Classes.Cliente import Cliente
from Classes.Pedido import Pedido
from Classes.Produto import Produto
from db_manager import adiciona_entrada, ultimo_id, imprime_todos_pedidos_completo, desativa_id, \
    desativa_nome, ativa_id, ativa_nome, modifica_documento

# Inicializa a conexão com o firestore
cred = credentials.Certificate('(...).json') # arquivo .json 
firebase_admin.initialize_app(cred)
db = firestore.client()


def get_input(lower_limit, higher_limit, prompt=''):
    value = input(prompt)
    while not value.isnumeric() or not lower_limit <= int(value) <= higher_limit:
        print(f"'{value}' não está entre {lower_limit} e {higher_limit}")
        value = input(f"Entre com um numero entre {lower_limit} a {higher_limit}: ")
    return int(value)


def get_input_in_list(user_list, prompt=''):
    value = input(prompt)
    while value not in user_list:
        value = input(f"Entre com um valor que esteja em {user_list}: ")
    return str(value)


def op_adicionar_entrada():
    def adicionar_cliente():
        nome = str(input('Entre com um nome: '))
        idade = get_input(0, 130, 'Entre com a idade: ')
        sexo = str(input('Entre com o sexo: '))
        rua = str(input('Entre com a rua: '))
        numero = str(input('Entre com o numero: '))
        bairro = str(input('Entre com o bairro: '))
        cidade = str(input('Entre com a cidade: '))
        estado = str(input('Entre com o estado: '))
        cep = str(input('Entre com o cep: '))
        referencia = str(input('Entre com a referencia: '))
        novo_cliente = Cliente(nome, idade, sexo, rua, numero, bairro, cidade,
                               estado, cep, referencia, True)
        return novo_cliente

    def adicionar_pedido():
        max_id_cliente = ultimo_id('Pedido', db)
        max_id_produto = ultimo_id('Produto', db)
        id_cliente = get_input(0, max_id_cliente, 'Entre com o id do cliente: ')
        id_produto = get_input(0, max_id_produto, 'Entre com o id do produto comprado: ')
        qntd_produto = get_input(0, 1_000, 'Entre com a quantidade do produto comprado: ')
        tipo_pagamento = str(input('Entre com o tipo de pagamento do pedido: '))
        status_pagamento = str(input('Entre com o status do pagamento: '))
        status_entrega = str(input('Entre com o status da entrega: '))

        novo_pedido = Pedido(id_cliente, id_produto, qntd_produto, tipo_pagamento, status_pagamento,
                             status_entrega, True)

        if get_input(0, 1, 'Deseja adicionar mais algum produto comprado nesse pedido?'):
            quantos_novos_produtos = get_input(0, 10, 'Adicionar quantos novos produtos?')
            for i in range(quantos_novos_produtos):
                id_produto = get_input(0, max_id_produto, 'Entre com o id do produto comprado: ')
                qntd_produto = get_input(0, 1_000, 'Entre com a quantidade do produto comprado: ')
                novo_pedido.add_pedido(id_produto, qntd_produto)

        return novo_pedido

    def adicionar_produto():
        tipo = str(input('Entre com o tipo do produto: '))
        nome = str(input('Entre com o nome: '))
        cor = str(input('Entre com a cor: '))
        preco = get_input(10, 100_000, 'Entre com o preco: ')
        estoque = get_input(0, 10_000, 'Entre a quantidade que existe no estoque: ')
        material = str(input('Entre com o material: '))
        novo_produto = Produto(tipo, nome, cor, preco, estoque, material, True)
        return novo_produto

    def entradas():
        print('1. Adicionar um Cliente')
        print('2. Adicionar um Pedido')
        print('3. Adicionar um Produto')
        print('0. Voltar')

    entradas()
    op = get_input(0, 3, 'Selecione uma opção: ')
    while op != 0:
        if op == 1:
            adiciona_entrada(adicionar_cliente(), db)
        if op == 2:
            adiciona_entrada(adicionar_pedido(), db)
        if op == 3:
            adiciona_entrada(adicionar_produto(), db)
        if op == 0:
            return
        entradas()
        op = get_input(0, 3, 'Selecione uma opção: ')


def op_modificar_entrada():
    collection = get_input_in_list(['Cliente', 'Pedido', 'Produto'],
                                   prompt='Deseja modificar um Cliente, Pedido ou Produto: ')
    max_id = ultimo_id(collection, db)
    qual_id = get_input(0, max_id, 'Entre com um id para modificar: ')
    changes_dict = {}
    if collection == 'Cliente':
        possible_names = globals()[collection]().__dict__.keys()
        key = get_input_in_list(possible_names, prompt='Qual chave vai alterar: ')
        if key == 'idade':
            mod = get_input(0, 130, 'Entre com a idade: ')
        else:
            mod = str(input('Entre o valor: '))
        changes_dict = {key: mod}
    elif collection == 'Produto':
        possible_names = globals()[collection]().__dict__.keys()
        key = get_input_in_list(possible_names, prompt='Qual chave vai alterar: ')
        if key == 'preco':
            mod = get_input(10, 100_000, 'Entre com o preco: ')
        elif key == 'estoque':
            mod = get_input(0, 10_000, 'Entre a quantidade que existe no estoque: ')
        else:
            mod = str(input('Entre o valor: '))
        changes_dict = {key: mod}
    elif collection == 'Pedido':
        key = get_input_in_list(['statusPagamento', 'statusEntrega'],
                                prompt='Qual chave vai alterar: ')
        mod = str(input('Entre o valor: '))
        changes_dict = {key: mod}
    modifica_documento(qual_id, changes_dict, collection, db)


def op_desativar_entrada():
    def desativar_por_id():
        collection = get_input_in_list(['Cliente', 'Pedido', 'Produto'],
                                       prompt='Deseja desativar um Cliente, Pedido ou Produto: ')
        max_id = ultimo_id(collection, db)
        qual_id = get_input(0, max_id, 'Entre com um id para desativar: ')
        desativa_id(qual_id, collection, db)

    def desativar_por_nome():
        collection = get_input_in_list(['Cliente', 'Pedido', 'Produto'],
                                       prompt='Deseja desativar um Cliente, Pedido ou Produto: ')
        nome = str(input('Entre com um nome para desativar: '))
        desativa_nome(nome, collection, db)

    def entradas():
        print('1. Desativar por id')
        print('2. Desativar por nome (todos que tiverem esse nome)')
        print('0. Voltar')

    entradas()
    op = get_input(0, 2, 'Selecione uma opção: ')
    while op != 0:
        if op == 1:
            desativar_por_id()
        if op == 2:
            desativar_por_nome()
        if op == 0:
            return
        entradas()
        op = get_input(0, 2, 'Selecione uma opção: ')


def op_ativar_entrada():
    def ativar_por_id():
        collection = get_input_in_list(['Cliente', 'Pedido', 'Produto'],
                                       prompt='Deseja ativar um Cliente, Pedido ou Produto: ')
        max_id = ultimo_id(collection, db)
        qual_id = get_input(0, max_id, 'Entre com um id para ativar: ')
        ativa_id(qual_id, collection, db)

    def ativar_por_nome():
        collection = get_input_in_list(['Cliente', 'Pedido', 'Produto'],
                                       prompt='Deseja ativar um Cliente, Pedido ou Produto: ')
        nome = str(input('Entre com um nome para ativar: '))
        ativa_nome(nome, collection, db)

    def entradas():
        print('1. Ativar por id')
        print('2. Ativar por nome (todos que tiverem esse nome)')
        print('0. Voltar')

    entradas()
    op = get_input(0, 2, 'Selecione uma opção: ')
    while op != 0:
        if op == 1:
            ativar_por_id()
        if op == 2:
            ativar_por_nome()
        if op == 0:
            return
        entradas()
        op = get_input(0, 2, 'Selecione uma opção: ')


def menu_usuario():
    def entradas():
        print('1. Adicionar uma nova entrada')
        print('2. Modificar uma entrada')
        print('3. Ativar uma entrada')
        print('4. Desativar uma entrada')
        print('5. Printar todos os pedidos completos (com cliente e produto)')
        print('0. Sair')

    entradas()
    op = get_input(0, 5, 'Selecione uma opção: ')
    while op != 0:
        if op == 1:
            op_adicionar_entrada()
        if op == 2:
            op_modificar_entrada()
        if op == 3:
            op_ativar_entrada()
        if op == 4:
            op_desativar_entrada()
        if op == 5:
            imprime_todos_pedidos_completo(db)
        if op == 0:
            sys.exit()
        entradas()
        op = get_input(0, 5, 'Selecione uma opção: ')


def main():
    menu_usuario()


if __name__ == "__main__":
    main()
