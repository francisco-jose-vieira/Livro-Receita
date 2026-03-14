class Receita:

    def __init__(self, nome, ingredientes, modo_preparo):
        self.nome = nome
        self.ingredientes = ingredientes
        self.modo_preparo = modo_preparo


    def texto_receita(self):

        texto = f"Receita: {self.nome}\n\n"

        texto += "Ingredientes:\n"
        for ingrediente in self.ingredientes:
            texto += f"- {ingrediente}\n"

        texto += "\nModo de preparo:\n"
        for i, passo in enumerate(self.modo_preparo):
            texto += f"{i+1} - {passo}\n"

        return texto