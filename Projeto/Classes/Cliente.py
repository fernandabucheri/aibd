class Cliente(object):
    def __init__(self, nome='', idade=0, sexo='', rua='', numero='', bairro='', cidade='',
                 estado='', cep='', referencia='', enabled=True):
        self.nome = nome
        self.idade = idade
        self.sexo = sexo
        self.endereco = self.asdict(rua, numero, bairro, cidade, estado, cep, referencia)
        self.enabled = enabled

    @staticmethod
    def asdict(rua, numero, bairro, cidade, estado, cep, referencia):
        return {'rua': rua, 'numero': numero, 'bairro': bairro,
                'cidade': cidade, 'estado': estado, 'cep': cep,
                'referencia': referencia}

    @staticmethod
    def from_dict(source):
        return Cliente(source['nome'], source['idade'], source['sexo'],
                       source['endereco']['rua'], source['endereco']['numero'],
                       source['endereco']['bairro'], source['endereco']['cidade'],
                       source['endereco']['estado'], source['endereco']['cep'],
                       source['endereco']['referencia'], source['enabled'])

    def __str__(self):
        return '{\n' \
               f'  nome: {self.nome},\n' \
               f'  idade: {self.idade},\n' \
               f'  sexo: {self.sexo},\n' \
               f'  enabled: {self.enabled},\n' \
               '  endereco: {\n' \
               f'      rua: {self.endereco["rua"]},\n' \
               f'      numero: {self.endereco["numero"]},\n' \
               f'      bairro: {self.endereco["bairro"]},\n' \
               f'      cidade: {self.endereco["cidade"]},\n' \
               f'      estado: {self.endereco["estado"]},\n' \
               f'      cep: {self.endereco["cep"]},\n' \
               f'      referencia: {self.endereco["referencia"]},\n' \
               '   },\n' \
               '}\n'
