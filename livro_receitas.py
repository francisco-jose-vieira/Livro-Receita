class LivroDeReceitas:

    def __init__(self):
        self.receitas = []


    def adicionar_receita(self, receita):
        self.receitas.append(receita)


    def remover_receita(self, indice):
        if 0 <= indice < len(self.receitas):
            self.receitas.pop(indice)


    def obter_receitas(self):
        return self.receitas