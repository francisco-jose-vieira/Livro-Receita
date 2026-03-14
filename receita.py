class Receita:
    def __init__(self, nome, ingredientes, modo_preparo, tempo="--", porcoes="--", foto_path=None):
        self.nome = nome
        self.ingredientes = ingredientes
        self.modo_preparo = modo_preparo
        self.tempo = tempo
        self.porcoes = porcoes
        self.foto_path = foto_path

    def texto_receita(self):
        texto = f"Receita: {self.nome}\n"
        texto += f"⏱ Tempo: {self.tempo} | 🍴 Porções: {self.porcoes}\n\n"
        
        texto += "INGREDIENTES\n"
        for ing in self.ingredientes:
            if ing.strip():
                texto += f"• {ing}\n"

        texto += "\nMODO DE PREPARO\n"
        for i, passo in enumerate(self.modo_preparo):
            if passo.strip():
                texto += f"{i+1}. {passo}\n"

        return texto