import os

import customtkinter as ctk
from PIL import Image


def _apenas_numeros(texto: str) -> bool:
    return texto == "" or texto.isdigit()


class FormularioView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._entradas_ingredientes: list[ctk.CTkEntry] = []
        self._entradas_modo: list[ctk.CTkEntry] = []
        self._container_ing: ctk.CTkFrame | None = None
        self._container_modo: ctk.CTkFrame | None = None
        self._frame_foto: ctk.CTkFrame | None = None
        self._in_nome: ctk.CTkEntry | None = None
        self._in_tempo: ctk.CTkEntry | None = None
        self._in_porcao: ctk.CTkEntry | None = None

    def renderizar(self, receita=None, indice: int | None = None):
        self._entradas_ingredientes = []
        self._entradas_modo = []

        for w in self.winfo_children():
            w.destroy()

        wrap = ctk.CTkScrollableFrame(self, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=40, pady=10)
        wrap.grid_columnconfigure(0, weight=1)

        titulo = "✏️  Editar Receita" if receita else "➕  Nova Receita"
        ctk.CTkLabel(wrap, text=titulo, font=("Arial Bold", 26)).pack(anchor="w", pady=(10, 4))
        ctk.CTkLabel(
            wrap,
            text="* Campos obrigatórios",
            font=("Arial", 11),
            text_color="#8D7B6D",
        ).pack(anchor="w", pady=(0, 14))

        self._build_foto(wrap, receita)
        self._build_campos_basicos(wrap, receita)
        self._build_ingredientes(wrap, receita)
        self._build_modo_preparo(wrap, receita)
        self._build_acoes(wrap, indice)

    def _build_foto(self, parent, receita):
        self._frame_foto = ctk.CTkFrame(
            parent,
            height=200,
            fg_color="#24170E",
            border_width=1,
            border_color="#3D2B1F",
            corner_radius=14,
        )
        self._frame_foto.pack(fill="x", pady=(0, 16))
        self._frame_foto.pack_propagate(False)

        if receita and receita.foto_path and os.path.exists(receita.foto_path):
            self._exibir_preview(receita.foto_path)
        else:
            self._exibir_placeholder()

    def _exibir_placeholder(self):
        for w in self._frame_foto.winfo_children():
            w.destroy()
        inner = ctk.CTkFrame(self._frame_foto, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(inner, text="📷", font=("Arial", 32)).pack()
        ctk.CTkButton(
            inner,
            text="Selecionar foto",
            fg_color="#3D2B1F",
            hover_color="#4D3525",
            height=36,
            corner_radius=8,
            command=self.controller.selecionar_foto,
        ).pack(pady=(8, 0))

    def _exibir_preview(self, caminho: str):
        for w in self._frame_foto.winfo_children():
            w.destroy()
        img = ctk.CTkImage(Image.open(caminho), size=(750, 198))
        lbl = ctk.CTkLabel(self._frame_foto, image=img, text="", corner_radius=14)
        lbl.pack(fill="both", expand=True)
        ctk.CTkButton(
            lbl,
            text="🔄 Alterar",
            fg_color="#222222",
            hover_color="#333333",
            height=32,
            width=110,
            corner_radius=8,
            command=self.controller.selecionar_foto,
        ).place(relx=1.0, rely=0.0, anchor="ne", x=-12, y=12)

    def atualizar_foto(self, caminho: str):
        self._exibir_preview(caminho)

    def _build_campos_basicos(self, parent, receita):
        ctk.CTkLabel(
            parent, text="Nome da Receita *", font=("Arial Bold", 13), text_color="#F5912E"
        ).pack(anchor="w")
        self._in_nome = ctk.CTkEntry(
            parent,
            placeholder_text="Ex: Bolo de Cenoura",
            height=48,
            fg_color="#24170E",
            border_color="#3D2B1F",
            corner_radius=10,
            font=("Arial", 14),
        )
        self._in_nome.pack(fill="x", pady=(4, 14))
        if receita:
            self._in_nome.insert(0, receita.nome)

        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=(0, 14))
        row.grid_columnconfigure((0, 1), weight=1)

        validar_num = (self.register(_apenas_numeros), "%P")

        for col_idx, (attr, label, ph, sufixo) in enumerate(
            [
                ("_in_tempo", "Tempo (minutos) *", "Ex: 45", " min"),
                ("_in_porcao", "Porções *", "Ex: 4", " porções"),
            ]
        ):
            frame = ctk.CTkFrame(row, fg_color="transparent")
            frame.grid(row=0, column=col_idx, sticky="ew", padx=(0 if col_idx == 0 else 8, 0))
            ctk.CTkLabel(
                frame, text=label, font=("Arial Bold", 13), text_color="#F5912E"
            ).pack(anchor="w")
            entry = ctk.CTkEntry(
                frame,
                placeholder_text=ph,
                height=48,
                fg_color="#24170E",
                border_color="#3D2B1F",
                corner_radius=10,
                font=("Arial", 14),
                validate="key",
                validatecommand=validar_num,
            )
            entry.pack(fill="x", pady=(4, 0))
            if receita:
                valor = getattr(receita, "tempo" if col_idx == 0 else "porcoes", "")
                entry.insert(0, valor.replace(sufixo, ""))
            setattr(self, attr, entry)

    def _build_ingredientes(self, parent, receita):
        ctk.CTkLabel(
            parent, text="📝 Ingredientes", font=("Arial Bold", 18), text_color="#F5912E"
        ).pack(anchor="w", pady=(6, 4))

        self._container_ing = ctk.CTkFrame(parent, fg_color="transparent")
        self._container_ing.pack(fill="x")

        itens = receita.ingredientes if receita else []
        if itens:
            for texto in itens:
                self._add_campo(self._container_ing, self._entradas_ingredientes, "ing", texto)
        else:
            self._add_campo(self._container_ing, self._entradas_ingredientes, "ing")

        ctk.CTkButton(
            parent,
            text="＋ Ingrediente",
            fg_color="transparent",
            text_color="#F5912E",
            hover_color="#2a1a10",
            border_width=1,
            border_color="#3D2B1F",
            height=40,
            corner_radius=8,
            command=lambda: self._add_campo(
                self._container_ing, self._entradas_ingredientes, "ing"
            ),
        ).pack(fill="x", pady=(8, 16))

    def _build_modo_preparo(self, parent, receita):
        ctk.CTkLabel(
            parent, text="🥣 Modo de Preparo", font=("Arial Bold", 18), text_color="#F5912E"
        ).pack(anchor="w", pady=(6, 4))

        self._container_modo = ctk.CTkFrame(parent, fg_color="transparent")
        self._container_modo.pack(fill="x")

        itens = receita.modo_preparo if receita else []
        if itens:
            for texto in itens:
                self._add_campo(self._container_modo, self._entradas_modo, "modo", texto)
        else:
            self._add_campo(self._container_modo, self._entradas_modo, "modo")

        ctk.CTkButton(
            parent,
            text="＋ Passo",
            fg_color="transparent",
            text_color="#F5912E",
            hover_color="#2a1a10",
            border_width=1,
            border_color="#3D2B1F",
            height=40,
            corner_radius=8,
            command=lambda: self._add_campo(
                self._container_modo, self._entradas_modo, "modo"
            ),
        ).pack(fill="x", pady=(8, 16))

    def _build_acoes(self, parent, indice):
        ctk.CTkButton(
            parent,
            text="💾  Salvar Receita",
            fg_color="#F5912E",
            hover_color="#e07d1c",
            text_color="black",
            font=("Arial Bold", 16),
            height=54,
            corner_radius=12,
            command=lambda: self.controller.salvar_receita(indice),
        ).pack(fill="x", pady=(10, 8))

        ctk.CTkButton(
            parent,
            text="Cancelar",
            fg_color="transparent",
            text_color="#8D7B6D",
            hover_color="#2a1a10",
            height=38,
            corner_radius=8,
            command=self.controller.criar_tela_principal,
        ).pack(pady=(0, 20))

    def _add_campo(self, container, lista, tipo, texto=""):
        idx = len(lista) + 1
        frame = ctk.CTkFrame(container, fg_color="transparent")
        frame.pack(fill="x", pady=4)

        ctk.CTkLabel(
            frame,
            text=f"{idx}.",
            font=("Arial Bold", 13),
            text_color="#F5912E",
            width=28,
        ).pack(side="left", padx=(0, 8))

        ph = "Ex: 500g de farinha" if tipo == "ing" else "Ex: Misture todos os secos..."
        entry = ctk.CTkEntry(
            frame,
            placeholder_text=ph,
            height=44,
            fg_color="#24170E",
            border_color="#3D2B1F",
            corner_radius=8,
            font=("Arial", 13),
        )
        if texto:
            entry.insert(0, texto)
        entry.pack(side="left", fill="x", expand=True)
        lista.append(entry)

        ctk.CTkButton(
            frame,
            text="🗑",
            width=40,
            height=44,
            fg_color="transparent",
            text_color="#E74C3C",
            hover_color="#2a1212",
            corner_radius=8,
            command=lambda: self._remover_campo(frame, entry, lista, container),
        ).pack(side="right", padx=(8, 0))

    def _remover_campo(self, frame, entry, lista, container):
        if entry in lista:
            lista.remove(entry)
        frame.destroy()
        self._renumerar(container)

    def _renumerar(self, container):
        for idx, child in enumerate(container.winfo_children(), start=1):
            for sub in child.winfo_children():
                if isinstance(sub, ctk.CTkLabel):
                    sub.configure(text=f"{idx}.")
                    break

    @property
    def nome(self) -> str:
        return self._in_nome.get().strip() if self._in_nome else ""

    @property
    def tempo(self) -> str:
        return self._in_tempo.get().strip() if self._in_tempo else ""

    @property
    def porcoes(self) -> str:
        return self._in_porcao.get().strip() if self._in_porcao else ""

    @property
    def ingredientes(self) -> list[str]:
        return [e.get().strip() for e in self._entradas_ingredientes if e.get().strip()]

    @property
    def modo_preparo(self) -> list[str]:
        return [e.get().strip() for e in self._entradas_modo if e.get().strip()]
