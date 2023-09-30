class Produto(object):
    def __init__(self, tipo='', nome='', cor='', preco=0, emEstoque=0, material='', enabled=True):
        self.tipo = tipo
        self.nome = nome
        self.cor = cor
        self.preco = preco
        self.emEstoque = emEstoque
        self.material = material
        self.enabled = enabled

    @staticmethod
    def from_dict(source):
        return Produto(source['tipo'], source['nome'], source['cor'], source['preco'],
                       source['emEstoque'], source['material'], source['enabled'])

    def __str__(self):
        return '{\n' \
               f'  tipo: {self.tipo},\n' \
               f'  nome: {self.nome},\n' \
               f'  enabled: {self.enabled},\n' \
               f'  cor: {self.cor},\n' \
               f'  preco: {self.preco},\n' \
               f'  emEstoque: {self.emEstoque},\n' \
               f'  material: {self.material}\n' \
               '}'
