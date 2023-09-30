class Pedido(object):
    def __init__(self, idCliente=0, idProduto=0, qntdProduto=0, tipoPagamento='',
                 statusPagamento='', statusEntrega='', enabled=True):
        self.idCliente = idCliente
        self.produtosPedidos = [{'idProduto': idProduto, 'qntdProduto': qntdProduto}]
        self.tipoPagamento = tipoPagamento
        self.statusPagamento = statusPagamento
        self.statusEntrega = statusEntrega
        self.enabled = enabled

    def add_pedido(self, idProduto, qntdProduto):
        self.produtosPedidos.append({'idProduto': idProduto, 'qntdProduto': qntdProduto})

    @staticmethod
    def from_dict(source):
        lista_produtos_pedidos = source.get('produtosPedidos')

        # Define os atributos dos produtosPedidos direto no dict do documento
        source['idProduto'] = lista_produtos_pedidos[0].get('idProduto')
        source['qntdProduto'] = lista_produtos_pedidos[0].get('qntdProduto')

        # Cria uma classe passando os atributos na ordem correta
        pedido = Pedido(source['idCliente'], source['idProduto'], source['qntdProduto'],
                        source['tipoPagamento'], source['statusPagamento'],
                        source['statusEntrega'], source['enabled'])

        # Remove o primeiro elemento da lista que já foi adicionado à classe
        lista_produtos_pedidos.pop(0)

        # Passa por todos os dicts na lista para adicionar na classe criada
        for produtoPedido in lista_produtos_pedidos:
            pedido.add_pedido(produtoPedido.get('idProduto'), produtoPedido.get('qntdProduto'))
        return pedido

    def __str__(self):
        produtos_pedidos = '   produtosPedidos: [ \n'
        for _ in self.produtosPedidos:
            produtos_pedidos += '       {\n' \
                                f'          idProduto: {_.get("idProduto")}, \n' \
                                f'          qntdProduto: {_.get("qntdProduto")} \n' \
                                '       },\n'
        produtos_pedidos += '   ],'
        return '{\n' \
               f'   idCliente: {self.idCliente}, \n' \
               f'   enabled: {self.enabled}, \n' \
               f'{produtos_pedidos} \n' \
               f'   tipoPagamento: {self.tipoPagamento}, \n' \
               f'   statusPagamento: {self.statusPagamento}, \n' \
               f'   statusEntrega: {self.statusEntrega},\n' \
               '}\n'