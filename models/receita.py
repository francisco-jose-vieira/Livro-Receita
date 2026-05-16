class Receita:
    def __init__(
        self,
        nome: str,
        ingredientes: list[str],
        modo_preparo: list[str],
        tempo: str = "--",
        porcoes: str = "--",
        foto_path: str | None = None,
        checklist: dict[str, bool] | None = None,
    ):
        self.nome = nome
        self.ingredientes = ingredientes
        self.modo_preparo = modo_preparo
        self.tempo = tempo
        self.porcoes = porcoes
        self.foto_path = foto_path
        self.checklist: dict[str, bool] = checklist or {}

    def to_dict(self) -> dict:
        return {
            "nome": self.nome,
            "ingredientes": self.ingredientes,
            "modo_preparo": self.modo_preparo,
            "tempo": self.tempo,
            "porcoes": self.porcoes,
            "foto_path": self.foto_path,
            "checklist": self.checklist,
        }
