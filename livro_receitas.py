import json
import os
from receita import Receita

class LivroDeReceitas:
    def __init__(self):
        self.pasta_db = "DB"
        self.arquivo_db = os.path.join(self.pasta_db, "receitas.json")
        self.receitas = []
        
        self._inicializar_banco_dados()
        self.carregar_receitas()

    def _inicializar_banco_dados(self):
        if not os.path.exists(self.pasta_db):
            os.makedirs(self.pasta_db)
        if not os.path.exists(self.arquivo_db):
            self.salvar_em_disco()

    def salvar_em_disco(self):
        with open(self.arquivo_db, "w", encoding="utf-8") as f:
            dados = [r.to_dict() for r in self.receitas]
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def carregar_receitas(self):
        if os.path.exists(self.arquivo_db):
            try:
                with open(self.arquivo_db, "r", encoding="utf-8") as f:
                    conteudo = f.read()
                    if conteudo:
                        dados = json.loads(conteudo)
                        self.receitas = [Receita(**item) for item in dados]
            except Exception as e:
                print(f"Erro ao carregar: {e}")
                self.receitas = []

    def adicionar_receita(self, receita):
        self.receitas.append(receita)
        self.salvar_em_disco()

    def remover_receita(self, indice):
        if 0 <= indice < len(self.receitas):
            self.receitas.pop(indice)
            self.salvar_em_disco()

    def obter_receitas(self):
        return self.receitas