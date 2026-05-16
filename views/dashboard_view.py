import os

import customtkinter as ctk
from PIL import Image


class DashboardView(ctk.CTkFrame):
    _BREAKPOINTS = (900, 600)

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._colunas_atuais = 3
        self._cards_data: list = []

        self._build_header()
        self._build_grid_area()
        self.bind("<Configure>", self._on_resize)

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(30, 10))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")
        ctk.CTkLabel(left, text="Minhas Receitas", font=("Arial Bold", 28)).pack(anchor="w")
        ctk.CTkLabel(
            left,
            text="Gerencie suas criações favoritas",
            font=("Arial", 13),
            text_color="#8D7B6D",
        ).pack(anchor="w")

        ctk.CTkButton(
            header,
            text="＋  Adicionar Receita",
            fg_color="#F5912E",
            hover_color="#e07d1c",
            text_color="black",
            font=("Arial Bold", 14),
            height=42,
            corner_radius=10,
            command=self.controller.tela_adicionar,
        ).pack(side="right")

    def _build_grid_area(self):
        self._scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._scroll.pack(fill="both", expand=True, padx=30, pady=10)

    def renderizar(self, receitas: list):
        self._cards_data = receitas
        self._limpar_grid()

        if not receitas:
            ctk.CTkLabel(
                self._scroll,
                text="Nenhuma receita encontrada.\nClique em '＋ Adicionar Receita' para começar.",
                font=("Arial", 16, "italic"),
                text_color="#8D7B6D",
                justify="center",
            ).pack(expand=True, pady=80)
            return

        self._redesenhar_cards(self._colunas_atuais)

    def _limpar_grid(self):
        for w in self._scroll.winfo_children():
            w.destroy()

    def _redesenhar_cards(self, colunas: int):
        self._limpar_grid()
        for c in range(colunas):
            self._scroll.grid_columnconfigure(c, weight=1, uniform="col")

        for idx, receita in enumerate(self._cards_data):
            self._criar_card(receita, idx, colunas)

    def _criar_card(self, receita, indice: int, colunas: int):
        card = ctk.CTkFrame(self._scroll, fg_color="#24170E", corner_radius=15)
        card.grid(
            row=indice // colunas,
            column=indice % colunas,
            padx=10,
            pady=10,
            sticky="nsew",
        )

        thumb_w, thumb_h = 320, 160
        if receita.foto_path and os.path.exists(receita.foto_path):
            try:
                pil = Image.open(receita.foto_path)
                fator = max(thumb_w / pil.width, thumb_h / pil.height)
                nw, nh = int(pil.width * fator), int(pil.height * fator)
                pil = pil.resize((nw, nh), Image.LANCZOS)
                left, top = (nw - thumb_w) // 2, (nh - thumb_h) // 2
                pil = pil.crop((left, top, left + thumb_w, top + thumb_h))
                img_ctk = ctk.CTkImage(pil, size=(thumb_w, thumb_h))
                ctk.CTkLabel(card, image=img_ctk, text="").pack(fill="x")
            except Exception:
                self._thumb_placeholder(card, thumb_h)
        else:
            self._thumb_placeholder(card, thumb_h)

        ctk.CTkLabel(
            card, text=receita.nome, font=("Arial Bold", 16), wraplength=250
        ).pack(anchor="w", padx=16, pady=(12, 2))
        ctk.CTkLabel(
            card,
            text=f"⏱ {receita.tempo}   🍴 {receita.porcoes}",
            font=("Arial", 11),
            text_color="#F5912E",
        ).pack(anchor="w", padx=16, pady=(0, 10))

        ctk.CTkButton(
            card,
            text="Ver Receita",
            fg_color="#38261A",
            hover_color="#4D3525",
            height=38,
            corner_radius=8,
            command=lambda i=indice: self.controller.ver_receita(i),
        ).pack(fill="x", padx=16, pady=(4, 6))

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=(0, 16))
        ctk.CTkButton(
            btn_row,
            text="✎ Editar",
            fg_color="transparent",
            border_width=1,
            border_color="#3D2B1F",
            height=34,
            corner_radius=8,
            command=lambda i=indice: self.controller.editar_receita(i),
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))
        ctk.CTkButton(
            btn_row,
            text="🗑",
            fg_color="transparent",
            text_color="#E74C3C",
            hover_color="#2a1212",
            width=38,
            height=34,
            corner_radius=8,
            command=lambda i=indice: self.controller.remover_receita(i),
        ).pack(side="right")

    @staticmethod
    def _thumb_placeholder(parent, altura: int):
        f = ctk.CTkFrame(parent, height=altura, fg_color="#3D2B1F", corner_radius=15)
        f.pack(fill="x")
        f.pack_propagate(False)
        ctk.CTkLabel(f, text="🍽", font=("Arial", 38)).place(relx=0.5, rely=0.5, anchor="center")

    def _on_resize(self, event):
        largura = event.width
        if largura >= self._BREAKPOINTS[0]:
            novas_colunas = 3
        elif largura >= self._BREAKPOINTS[1]:
            novas_colunas = 2
        else:
            novas_colunas = 1

        if novas_colunas != self._colunas_atuais and self._cards_data:
            self._colunas_atuais = novas_colunas
            self._redesenhar_cards(novas_colunas)
