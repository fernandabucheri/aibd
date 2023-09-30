from Classes.Cliente import Cliente
from Classes.Pedido import Pedido
from Classes.Produto import Produto


def ultimo_id(collection, db):
    # Abre uma conexão com essa classe no firestore
    connection = db.collection(collection)

    # Recebe qual foi o último id adicionado nessa coleção
    return connection.document('-1').get().to_dict().get('ultimoId')


def inicializa_conexao(entrada, db):
    # Pega o nome da collection a partir do nome da classe
    collection_name = entrada.__class__.__name__

    # Abre uma conexão com essa classe no firestore
    connection = db.collection(collection_name)

    # Recebe qual foi o último id adicionado nessa coleção
    document_id = connection.document('-1').get().to_dict().get('ultimoId')

    return connection, document_id


def adiciona_entrada(nova_entrada, db):
    connection, document_id = inicializa_conexao(nova_entrada, db)

    # Adiciona um à esse id e transforma pra string novamente
    document_id = str(document_id + 1)

    # Adiciona uma nova entrada no id definido
    connection.document(document_id).set(vars(nova_entrada))

    print(f"Entrada adicionada!")

    # Aumenta em 1 o último id adicionado
    connection.document('-1').update({'ultimoId': int(document_id)})


def encontra_id(id, collection, db):
    try:
        # Abre uma conexão com essa collection no firestore
        connection = db.collection(collection)

        # Acessa o documento com o id especificado
        doc = connection.document(str(id))
        if doc.get().exists:
            return connection, doc
        return None
    except Exception as e:
        print(e)


def modifica_documento(id, changes_dict, collection, db):
    connection, doc = encontra_id(id, collection, db)

    if doc is None:
        print('Id não encontrado!')
        return 1

    print('O documento a seguir vai ser modificado:')
    print(doc.get().to_dict())

    # Pega todas os atributos da coleção que o usuário quer alterar
    possible_names = globals()[collection]().__dict__.keys()

    lista_endereco = ['rua', 'numero', 'bairro', 'cidade', 'estado', 'cep', 'referencia']

    if collection == 'Cliente':
        endereco_atual = doc.get().to_dict().get('endereco')

    # Passa por todas as entradas das mudanças no changes_dict
    for key in changes_dict.keys():
        # Checa se essa chave da entrada é válida para essa coleção
        if key in possible_names:
            # Nos casos do endereco e produtosPedidos, verifica se os atributos correspondem ao \
            # esperado e atualizam o request do usuário
            if key == 'endereco' and collection == 'Cliente':
                for atributo in changes_dict.get(key):
                    if atributo in lista_endereco:
                        endereco_atual[atributo] = changes_dict.get(key).get(atributo)
                    else:
                        print(f'{atributo} não é um atributo do endereco e foi desconsiderado')

                # Atualiza a mudança do endereço no endereço atual do documento
                changes_dict[key] = endereco_atual

            # Atualiza esse atributo
            doc.update({key: changes_dict.get(key)})

    print('O documento foi alterado:')
    print(doc.get().to_dict())
    return 0


def deleta_id(id, collection, db):
    connection, doc = encontra_id(id, collection, db)

    if doc is None:
        return 'Id não encontrado!'

    deleted = doc.get().to_dict()
    doc.delete()

    print('O documento a seguir foi deletado:')
    print(deleted)

    print('Documento deletado')


def deleta_nome(nome, collection, db):
    if collection == 'Pedido':
        return 'A collection Pedido não possui o atributo nome'

    # Abre uma conexão com essa classe no firestore
    connection = db.collection(collection)

    try:
        # Recebe todos os documentos com o filtro passado
        docs = connection.where("nome", "==", nome).get()
        for doc in docs:
            # Verifica se o documento existe antes de tentar deletar
            if doc.exists:
                deleted = doc.to_dict()
                connection.document(doc.id).delete()
                print('O documento a seguir foi deletado:')
                print(deleted)
            else:
                print('Nome não encontrado!')
                return
        print('Todas as entradas foram deletadas')
    except Exception as e:
        print(e)


def desativa_id(id, collection, db):
    connection, doc = encontra_id(id, collection, db)

    if doc is None:
        return 'Id não encontrado!'

    deleted = doc.get().to_dict()
    doc.update({'enabled': False})

    print('O documento a seguir foi desativado (enabled setado para false):')
    print(deleted)

    print('Documento desativado')


def desativa_nome(nome, collection, db):
    if collection == 'Pedido':
        return 'A collection Pedido não possui o atributo nome'

    # Abre uma conexão com essa classe no firestore
    connection = db.collection(collection)

    try:
        # Recebe todos os documentos com o filtro passado
        docs = connection.where("nome", "==", nome).get()
        for doc in docs:
            # Verifica se o documento existe antes de tentar deletar
            if doc.exists:
                deleted = doc.to_dict()
                connection.document(doc.id).update({'enabled': False})
                print('O documento a seguir foi desativado (enabled setado para false):')
                print(deleted)
            else:
                print('Nome não encontrado!')
                return
        print('Todas as entradas foram desativadas')
    except Exception as e:
        print(e)


def ativa_id(id, collection, db):
    connection, doc = encontra_id(id, collection, db)

    if doc is None:
        return 'Id não encontrado!'

    deleted = doc.get().to_dict()
    doc.update({'enabled': True})

    print('O documento a seguir foi ativado (enabled setado para true):')
    print(deleted)

    print('Documento ativado')


def ativa_nome(nome, collection, db):
    if collection == 'Pedido':
        return 'A collection Pedido não possui o atributo nome'

    # Abre uma conexão com essa classe no firestore
    connection = db.collection(collection)

    try:
        # Recebe todos os documentos com o filtro passado
        docs = connection.where("nome", "==", nome).get()
        for doc in docs:
            # Verifica se o documento existe antes de tentar deletar
            if doc.exists:
                deleted = doc.to_dict()
                connection.document(doc.id).update({'enabled': True})
                print('O documento a seguir foi ativado (enabled setado para true):')
                print(deleted)
            else:
                print('Nome não encontrado!')
                return
        print('Todas as entradas foram ativadas')
    except Exception as e:
        print(e)


def imprime_todos_pedidos_completo(db):
    try:
        # Abre uma conexão com essa collection no firestore
        connection = db.collection('Pedido')

        # Acessa todos os documentos de pedidos existentes
        docs = connection.get()

        for doc in docs:
            if doc.exists and doc.id != '-1':
                # Transforma o documento para dicionário
                doc_dict = doc.to_dict()

                # Cria uma classe a partir desse dicionário
                pedido = Pedido.from_dict(doc_dict)

                # Procura pelo cliente correspondente ao pedido e passa pra uma classe
                matching_cliente = db.collection('Cliente').document(
                    str(doc_dict['idCliente'])).get().to_dict()
                classe_cliente = Cliente.from_dict(matching_cliente)

                # Cria uma lista de classe dos produtos pedidos nesse pedido
                matching_produtos = []
                for produto in pedido.produtosPedidos:
                    matching_produto = db.collection('Produto').document(
                        str(produto['idProduto'])).get().to_dict()
                    produto_classe = Produto.from_dict(matching_produto)
                    matching_produtos.append(produto_classe)
                print('-------------------------------\n')
                print("Pedido: ")
                print(str(pedido))
                print('Cliente:')
                print(str(classe_cliente))
                print('Produtos pedidos:')
                for produto in matching_produtos:
                    print(str(produto))

    except Exception as e:
        print(e)
