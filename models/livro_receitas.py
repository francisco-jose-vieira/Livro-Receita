import json
import os

from models.receita import Receita


class PersistenciaJSON:
    def __init__(self, pasta: str = "DB", arquivo: str = "receitas.json"):
        self.caminho = os.path.join(pasta, arquivo)
        os.makedirs(pasta, exist_ok=True)

    def salvar(self, receitas: list[Receita]) -> None:
        with open(self.caminho, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in receitas], f, indent=4, ensure_ascii=False)

    def carregar(self) -> list[Receita]:
        if not os.path.exists(self.caminho):
            return []
        try:
            with open(self.caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return [Receita(**item) for item in dados]
        except (json.JSONDecodeError, TypeError, KeyError):
            return []


class LivroDeReceitas:
    def __init__(self, persistencia: PersistenciaJSON | None = None):
        self._persistencia = persistencia or PersistenciaJSON()
        self._receitas: list[Receita] = self._persistencia.carregar()

    def obter_receitas(self) -> list[Receita]:
        return list(self._receitas)

    def obter_receita(self, indice: int) -> Receita:
        return self._receitas[indice]

    def adicionar(self, receita: Receita) -> None:
        self._receitas.append(receita)
        self._salvar()

    def atualizar(self, indice: int, receita: Receita) -> None:
        self._receitas[indice] = receita
        self._salvar()

    def remover(self, indice: int) -> None:
        if 0 <= indice < len(self._receitas):
            self._receitas.pop(indice)
            self._salvar()

    def atualizar_checklist(self, indice: int, checklist: dict[str, bool]) -> None:
        self._receitas[indice].checklist = checklist
        self._salvar()

    def _salvar(self) -> None:
        self._persistencia.salvar(self._receitas)
