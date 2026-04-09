class Receita:
    def __init__(self, nome, ingredientes, modo_preparo, tempo="--", porcoes="--", foto_path=None):
        self.nome = nome
        self.ingredientes = ingredientes
        self.modo_preparo = modo_preparo
        self.tempo = tempo
        self.porcoes = porcoes
        self.foto_path = foto_path

    def to_dict(self):
        return {
            "nome": self.nome, "ingredientes": self.ingredientes,
            "modo_preparo": self.modo_preparo, "tempo": self.tempo,
            "porcoes": self.porcoes, "foto_path": self.foto_path
        }