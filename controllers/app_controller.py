from tkinter import filedialog, messagebox

import customtkinter as ctk

from models import LivroDeReceitas, Receita
from views import DashboardView, DetalhesView, FormularioView


class AppController:
    def __init__(self):
        self._livro = LivroDeReceitas()
        self._foto_temporaria: str | None = None

        self._root = self._criar_janela()
        self._main_frame = ctk.CTkFrame(self._root, fg_color="transparent")
        self._main_frame.pack(fill="both", expand=True)

        self._dash_view = DashboardView(self._main_frame, self)
        self._detalhes_view = DetalhesView(self._main_frame, self)
        self._form_view = FormularioView(self._main_frame, self)

        self.criar_tela_principal()

    @staticmethod
    def _criar_janela() -> ctk.CTk:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        root = ctk.CTk()
        root.title("Diário de Receitas")
        root.geometry("1100x820")
        root.minsize(480, 600)
        root.configure(fg_color="#1A120B")

        try:
            root.iconbitmap("icone_temp.ico")
        except Exception:
            pass

        return root

    def _ocultar_todas_views(self):
        for view in (self._dash_view, self._detalhes_view, self._form_view):
            view.pack_forget()

    def criar_tela_principal(self):
        self._ocultar_todas_views()
        self._dash_view.pack(fill="both", expand=True)
        self._dash_view.renderizar(self._livro.obter_receitas())

    def tela_adicionar(self):
        self._ocultar_todas_views()
        self._foto_temporaria = None
        self._form_view.pack(fill="both", expand=True)
        self._form_view.renderizar()

    def ver_receita(self, indice: int):
        self._ocultar_todas_views()
        receita = self._livro.obter_receita(indice)
        self._detalhes_view.pack(fill="both", expand=True)
        self._detalhes_view.renderizar(receita, indice)

    def editar_receita(self, indice: int):
        self._ocultar_todas_views()
        receita = self._livro.obter_receita(indice)
        self._foto_temporaria = receita.foto_path
        self._form_view.pack(fill="both", expand=True)
        self._form_view.renderizar(receita, indice)

    def selecionar_foto(self):
        caminho = filedialog.askopenfilename(
            title="Selecionar imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.webp")],
        )
        if caminho:
            self._foto_temporaria = caminho
            self._form_view.atualizar_foto(caminho)

    def salvar_receita(self, indice: int | None = None):
        f = self._form_view

        if not f.nome:
            messagebox.showwarning("Campo obrigatório", "Informe o nome da receita.")
            return
        if not f.tempo:
            messagebox.showwarning("Campo obrigatório", "Informe o tempo de preparo.")
            return
        if not f.porcoes:
            messagebox.showwarning("Campo obrigatório", "Informe o número de porções.")
            return
        if not f.ingredientes:
            messagebox.showwarning("Campo obrigatório", "Adicione ao menos um ingrediente.")
            return
        if not f.modo_preparo:
            messagebox.showwarning("Campo obrigatório", "Adicione ao menos um passo de preparo.")
            return

        nova = Receita(
            nome=f.nome,
            ingredientes=f.ingredientes,
            modo_preparo=f.modo_preparo,
            tempo=f"{f.tempo} min",
            porcoes=f"{f.porcoes} porções",
            foto_path=self._foto_temporaria,
            checklist={},
        )

        if indice is not None:
            self._livro.atualizar(indice, nova)
        else:
            self._livro.adicionar(nova)

        self.criar_tela_principal()

    def remover_receita(self, indice: int):
        receita = self._livro.obter_receita(indice)
        confirmar = messagebox.askyesno(
            "Excluir receita",
            f"Deseja remover '{receita.nome}'?\nEsta ação não pode ser desfeita.",
        )
        if confirmar:
            self._livro.remover(indice)
            self.criar_tela_principal()

    def salvar_checklist(self, indice: int, checklist: dict[str, bool]):
        self._livro.atualizar_checklist(indice, checklist)

    def executar(self):
        self._root.mainloop()
