import os

import customtkinter as ctk
from PIL import Image

_BANNER_H = 260


def _cover_crop(pil_img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    fator = max(target_w / pil_img.width, target_h / pil_img.height)
    nw = int(pil_img.width * fator)
    nh = int(pil_img.height * fator)
    pil_img = pil_img.resize((nw, nh), Image.LANCZOS)
    left = (nw - target_w) // 2
    top = (nh - target_h) // 2
    return pil_img.crop((left, top, left + target_w, top + target_h))


class DetalhesView(ctk.CTkFrame):
    _BREAKPOINT_EMPILHAR = 680

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._indice: int = 0
        self._checklist_vars: dict[str, ctk.BooleanVar] = {}
        self._receita_atual = None
        self._img_ref = None
        self._body_frame: ctk.CTkFrame | None = None
        self._layout_empilhado: bool | None = None

    def renderizar(self, receita, indice: int):
        self._indice = indice
        self._checklist_vars = {}
        self._receita_atual = receita
        self._img_ref = None
        self._layout_empilhado = None

        for w in self.winfo_children():
            w.destroy()

        self._scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._scroll.pack(fill="both", expand=True, padx=20, pady=10)

        self._build_banner(self._scroll, receita)
        self._build_info_pills(self._scroll, receita)
        self._build_body(self._scroll, receita)
        self._build_footer(self._scroll, indice)

        self.bind("<Configure>", self._on_resize)

    def _build_banner(self, parent, receita):
        if receita.foto_path and os.path.exists(receita.foto_path):
            self._build_banner_com_foto(parent, receita)
        else:
            self._build_banner_sem_foto(parent, receita)

    def _build_banner_com_foto(self, parent, receita):
        root = self.winfo_toplevel()
        root.update_idletasks()
        banner_w = max(400, root.winfo_width() - 80)
        banner_h = _BANNER_H

        try:
            pil_img = Image.open(receita.foto_path)
            pil_img = _cover_crop(pil_img, banner_w, banner_h)
            self._img_ref = ctk.CTkImage(pil_img, size=(banner_w, banner_h))
        except Exception:
            self._build_banner_sem_foto(parent, receita)
            return

        container = ctk.CTkFrame(
            parent, fg_color="#1e140c", corner_radius=16,
            height=banner_h, width=banner_w,
        )
        container.pack(fill="x", pady=(0, 16))
        container.pack_propagate(False)

        img_lbl = ctk.CTkLabel(container, image=self._img_ref, text="", corner_radius=16)
        img_lbl.place(relx=0, rely=0, relwidth=1, relheight=1)

        overlay = ctk.CTkFrame(container, fg_color="#111111", corner_radius=0, height=54)
        overlay.place(relx=0, rely=1.0, anchor="sw", relwidth=1.0)
        overlay.pack_propagate(False)
        ctk.CTkLabel(
            overlay,
            text=receita.nome,
            font=("Arial Bold", 24),
            text_color="white",
            anchor="w",
        ).pack(padx=20, fill="y", side="left")

    def _build_banner_sem_foto(self, parent, receita):
        ctk.CTkLabel(
            parent,
            text=receita.nome,
            font=("Arial Bold", 30),
            text_color="#F5912E",
            anchor="w",
        ).pack(pady=(10, 16), padx=10, anchor="w")

    def _build_info_pills(self, parent, receita):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=(0, 16))

        for emoji, label, valor in [
            ("⏱", "TEMPO", receita.tempo),
            ("🍴", "PORÇÕES", receita.porcoes),
        ]:
            pill = ctk.CTkFrame(
                row,
                fg_color="#24170E",
                corner_radius=14,
                border_width=1,
                border_color="#3D2B1F",
                height=80,
            )
            pill.pack(side="left", expand=True, fill="x", padx=8)
            pill.pack_propagate(False)
            ctk.CTkLabel(
                pill,
                text=f"{emoji} {label}",
                font=("Arial Bold", 11),
                text_color="#F5912E",
            ).pack(anchor="w", padx=20, pady=(14, 0))
            ctk.CTkLabel(pill, text=valor, font=("Arial Bold", 20)).pack(anchor="w", padx=20)

    def _build_body(self, parent, receita):
        self._body_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self._body_frame.pack(fill="both", expand=True, pady=10)
        self._renderizar_body_sidebyside(receita)

    def _renderizar_body_sidebyside(self, receita):
        for w in self._body_frame.winfo_children():
            w.destroy()
        self._body_frame.grid_columnconfigure(0, weight=1)
        self._body_frame.grid_columnconfigure(1, weight=1)

        col_ing = ctk.CTkFrame(self._body_frame, fg_color="transparent")
        col_ing.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self._build_ingredientes(col_ing, receita)

        col_modo = ctk.CTkFrame(
            self._body_frame,
            fg_color="#1e140c",
            corner_radius=16,
            border_width=1,
            border_color="#3D2B1F",
        )
        col_modo.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self._build_modo_preparo(col_modo, receita)

    def _renderizar_body_empilhado(self, receita):
        for w in self._body_frame.winfo_children():
            w.destroy()
        self._body_frame.grid_columnconfigure(0, weight=1)
        try:
            self._body_frame.grid_columnconfigure(1, weight=0)
        except Exception:
            pass

        col_ing = ctk.CTkFrame(self._body_frame, fg_color="transparent")
        col_ing.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        self._build_ingredientes(col_ing, receita)

        col_modo = ctk.CTkFrame(
            self._body_frame,
            fg_color="#1e140c",
            corner_radius=16,
            border_width=1,
            border_color="#3D2B1F",
        )
        col_modo.grid(row=1, column=0, sticky="nsew")
        self._build_modo_preparo(col_modo, receita)

    def _build_ingredientes(self, parent, receita):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(
            header, text="📝 Ingredientes", font=("Arial Bold", 20), text_color="#F5912E"
        ).pack(side="left")
        ctk.CTkButton(
            header,
            text="↺ Limpar",
            fg_color="transparent",
            text_color="#8D7B6D",
            hover_color="#2a1a10",
            font=("Arial", 11),
            height=26,
            width=70,
            corner_radius=6,
            command=self._limpar_checklist,
        ).pack(side="right")

        self._progress_label = ctk.CTkLabel(
            parent, text="", font=("Arial", 11), text_color="#8D7B6D"
        )
        self._progress_label.pack(anchor="w", pady=(0, 6))

        self._progress_bar = ctk.CTkProgressBar(
            parent, fg_color="#3D2B1F", progress_color="#F5912E", height=6, corner_radius=3
        )
        self._progress_bar.set(0)
        self._progress_bar.pack(fill="x", pady=(0, 12))

        for ing in receita.ingredientes:
            var = ctk.BooleanVar(value=receita.checklist.get(ing, False))
            self._checklist_vars[ing] = var
            ctk.CTkCheckBox(
                parent,
                text=ing,
                variable=var,
                font=("Arial", 14),
                fg_color="#F5912E",
                hover_color="#e07d1c",
                border_color="#8D7B6D",
                checkmark_color="black",
                command=self._on_checklist_change,
            ).pack(anchor="w", pady=5)

        self._atualizar_progresso()

    def _build_modo_preparo(self, parent, receita):
        ctk.CTkLabel(
            parent,
            text="🥣 Modo de Preparo",
            font=("Arial Bold", 20),
            text_color="#F5912E",
        ).pack(anchor="w", padx=24, pady=(20, 14))

        for i, passo in enumerate(receita.modo_preparo):
            step = ctk.CTkFrame(parent, fg_color="transparent")
            step.pack(fill="x", padx=24, pady=8)

            ctk.CTkLabel(
                step,
                text=str(i + 1),
                font=("Arial Bold", 12),
                fg_color="#F5912E",
                text_color="black",
                width=28,
                height=28,
                corner_radius=14,
            ).pack(side="left", anchor="n", padx=(0, 14), pady=2)

            lbl_passo = ctk.CTkLabel(
                step,
                text=passo,
                font=("Arial", 14),
                wraplength=300,
                justify="left",
                anchor="nw",
            )
            lbl_passo.pack(side="left", fill="x", expand=True)
            step.bind(
                "<Configure>",
                lambda e, lbl=lbl_passo: lbl.configure(wraplength=max(100, e.width - 60)),
            )

        ctk.CTkFrame(parent, height=16, fg_color="transparent").pack()

    def _build_footer(self, parent, indice: int):
        footer = ctk.CTkFrame(parent, fg_color="transparent")
        footer.pack(fill="x", pady=(20, 10))

        ctk.CTkButton(
            footer,
            text="← Voltar",
            fg_color="#38261A",
            hover_color="#4D3525",
            height=50,
            corner_radius=10,
            command=self.controller.criar_tela_principal,
        ).pack(side="left", expand=True, fill="x", padx=(0, 10))

        ctk.CTkButton(
            footer,
            text="✎ Editar",
            fg_color="#F5912E",
            hover_color="#e07d1c",
            text_color="black",
            height=50,
            corner_radius=10,
            command=lambda: self.controller.editar_receita(indice),
        ).pack(side="right", expand=True, fill="x", padx=(10, 0))

    def _on_resize(self, event):
        if self._body_frame is None or self._receita_atual is None:
            return
        empilhar = event.width < self._BREAKPOINT_EMPILHAR
        if empilhar == self._layout_empilhado:
            return
        self._layout_empilhado = empilhar
        self._checklist_vars = {}
        if empilhar:
            self._renderizar_body_empilhado(self._receita_atual)
        else:
            self._renderizar_body_sidebyside(self._receita_atual)

    def _on_checklist_change(self):
        estado = {ing: var.get() for ing, var in self._checklist_vars.items()}
        self.controller.salvar_checklist(self._indice, estado)
        self._atualizar_progresso()

    def _atualizar_progresso(self):
        total = len(self._checklist_vars)
        if total == 0:
            return
        marcados = sum(1 for v in self._checklist_vars.values() if v.get())
        self._progress_bar.set(marcados / total)
        self._progress_label.configure(
            text=f"{marcados} de {total} ingredientes separados"
        )

    def _limpar_checklist(self):
        for var in self._checklist_vars.values():
            var.set(False)
        self._on_checklist_change()
