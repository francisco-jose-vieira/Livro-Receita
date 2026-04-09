import json
import os
from receita import Receita

class PersistenciaJSON:
    def __init__(self):
        self.pasta_db = "DB"
        self.arquivo_db = os.path.join(self.pasta_db, "receitas.json")
        if not os.path.exists(self.pasta_db): 
            os.makedirs(self.pasta_db)

    def salvar(self, lista_receitas):
        with open(self.arquivo_db, "w", encoding="utf-8") as f:
            dados = [r.to_dict() for r in lista_receitas]
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def carregar(self):
        if not os.path.exists(self.arquivo_db): 
            return []
        try:
            with open(self.arquivo_db, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return [Receita(**item) for item in dados]
        except (json.JSONDecodeError, Exception):
            return []

class LivroDeReceitas:
    def __init__(self):
        self.persistencia = PersistenciaJSON()
        # Aqui ele carrega os dados usando a classe de persistência
        self.receitas = self.persistencia.carregar()

    def adicionar_receita(self, receita):
        self.receitas.append(receita)
        self.persistencia.salvar(self.receitas)

    def remover_receita(self, indice):
        if 0 <= indice < len(self.receitas):
            self.receitas.pop(indice)
            self.persistencia.salvar(self.receitas)

    # ESTE É O MÉTODO QUE ESTAVA FALTANDO NO SEU ERRO:
    def obter_receitas(self):
        return self.receitas