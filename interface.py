import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont
import os

from receita import Receita
from livro_receitas import LivroDeReceitas


class InterfaceReceitas:
    def __init__(self):
        self.livro = LivroDeReceitas()
        self.foto_selecionada = None
        self.entradas_ingredientes = []
        self.entradas_modo = []

        # Cores
        self.cor_fundo = "#1A120B"
        self.cor_card = "#24170E"
        self.cor_laranja = "#F5912E"
        self.cor_laranja_hover = "#FFB066"
        self.cor_texto_sec = "#8D7B6D"

        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.title("Diário de Receitas")
        self.root.geometry("1150x900")
        self.root.configure(fg_color=self.cor_fundo)

        # --- NOVA FUNÇÃO PARA O ÍCONE DA JANELA ---
        self.definir_icone_janela("🍴")  # Coloque o emoji que desejar aqui

        self.criar_tela_principal()

    def definir_icone_janela(self, emoji):
        """Gera um ícone temporário a partir de um emoji para a janela"""
        try:
            # Cria uma imagem pequena para o ícone
            img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # Tenta carregar uma fonte que suporte emoji (Windows usa Segoe UI Emoji)
            try:
                font = ImageFont.truetype("seguiemj.ttf", 50)
            except:
                font = ImageFont.load_default()

            # Desenha o emoji na imagem
            draw.text((32, 32), emoji, font=font, anchor="mm")

            # Salva como um arquivo de ícone temporário
            img.save("icone_temp.ico", format="ICO")
            self.root.after(200, lambda: self.root.iconbitmap("icone_temp.ico"))
        except Exception as e:
            print(f"Não foi possível definir o emoji como ícone: {e}")

    # --- RESTANTE DO CÓDIGO (DASHBOARD, VER RECEITA, FORMULÁRIOS) ---
    # (Mantendo as correções de centralização e lixeiras individuais que fizemos)

    def limpar_tela(self):
        self.entradas_ingredientes = []
        self.entradas_modo = []
        self.foto_selecionada = None
        for widget in self.root.winfo_children():
            widget.destroy()

    def selecionar_foto(self, container_foto):
        caminho = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.jpg *.png *.jpeg")]
        )
        if caminho:
            self.foto_selecionada = caminho
            for widget in container_foto.winfo_children():
                widget.destroy()
            img_pil = Image.open(caminho)
            img_pil.thumbnail((700, 300))
            img_ctk = ctk.CTkImage(
                light_image=img_pil, dark_image=img_pil, size=img_pil.size
            )
            ctk.CTkLabel(container_foto, image=img_ctk, text="").pack(
                expand=True, fill="both"
            )

    def adicionar_campo_ingrediente(self, container, texto=""):
        frame_linha = ctk.CTkFrame(container, fg_color="transparent")
        frame_linha.pack(fill="x", pady=5)
        num = len(self.entradas_ingredientes) + 1
        lbl_num = ctk.CTkLabel(
            frame_linha,
            text=f"{num}.",
            font=("Arial Bold", 16),
            text_color=self.cor_laranja,
        )
        lbl_num.pack(side="left", padx=(0, 10))
        entrada = ctk.CTkEntry(
            frame_linha,
            placeholder_text="Ex: Ingrediente",
            height=45,
            fg_color=self.cor_card,
            border_color="#3D2B1F",
        )
        entrada.insert(0, texto)
        entrada.pack(side="left", fill="x", expand=True)
        btn_del = ctk.CTkButton(
            frame_linha,
            text="🗑",
            width=40,
            height=45,
            fg_color="transparent",
            text_color="#E74C3C",
            command=lambda f=frame_linha, e=entrada: self.remover_linha(f, e, "ing"),
        )
        btn_del.pack(side="right", padx=(10, 0))
        self.entradas_ingredientes.append(entrada)

    def adicionar_campo_modo(self, container, texto=""):
        frame_linha = ctk.CTkFrame(container, fg_color="transparent")
        frame_linha.pack(fill="x", pady=5)
        num = len(self.entradas_modo) + 1
        lbl_num = ctk.CTkLabel(
            frame_linha,
            text=f"{num}.",
            font=("Arial Bold", 16),
            text_color=self.cor_laranja,
        )
        lbl_num.pack(side="left", padx=(0, 10))
        entrada = ctk.CTkEntry(
            frame_linha,
            placeholder_text="Ex: Passo do preparo",
            height=45,
            fg_color=self.cor_card,
            border_color="#3D2B1F",
        )
        entrada.insert(0, texto)
        entrada.pack(side="left", fill="x", expand=True)
        btn_del = ctk.CTkButton(
            frame_linha,
            text="🗑",
            width=40,
            height=45,
            fg_color="transparent",
            text_color="#E74C3C",
            command=lambda f=frame_linha, e=entrada: self.remover_linha(f, e, "modo"),
        )
        btn_del.pack(side="right", padx=(10, 0))
        self.entradas_modo.append(entrada)

    def remover_linha(self, frame, widget_entrada, tipo):
        if tipo == "ing":
            self.entradas_ingredientes.remove(widget_entrada)
        else:
            self.entradas_modo.remove(widget_entrada)
        frame.destroy()

    def criar_tela_principal(self):
        self.limpar_tela()
        main_container = ctk.CTkFrame(self.root, fg_color="transparent", width=1000)
        main_container.pack(pady=20, expand=True, fill="both")

        header = ctk.CTkFrame(main_container, fg_color="transparent")
        header.pack(fill="x", padx=60, pady=(40, 10))

        info_f = ctk.CTkFrame(header, fg_color="transparent")
        info_f.pack(side="left")
        ctk.CTkLabel(info_f, text="Minhas Receitas", font=("Arial Bold", 32)).pack(
            anchor="w"
        )
        ctk.CTkLabel(
            info_f,
            text="Gerencie suas criações favoritas",
            font=("Arial", 14),
            text_color=self.cor_texto_sec,
        ).pack(anchor="w")

        ctk.CTkButton(
            header,
            text="+ Adicionar Receita",
            fg_color=self.cor_laranja,
            hover_color=self.cor_laranja_hover,
            text_color="black",
            font=("Arial Bold", 15),
            height=45,
            corner_radius=10,
            command=self.tela_adicionar,
        ).pack(side="right")

        receitas = self.livro.obter_receitas()
        if not receitas:
            lbl = ctk.CTkLabel(
                main_container,
                text="Não há receitas cadastradas no momento",
                font=("Arial", 18, "italic"),
                text_color=self.cor_texto_sec,
            )
            lbl.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.scroll = ctk.CTkScrollableFrame(
                main_container, fg_color="transparent", width=1000, height=650
            )
            self.scroll.pack(fill="both", expand=True, padx=50, pady=20)
            self.scroll._scrollbar.grid_forget()
            self.scroll.grid_columnconfigure((0, 1, 2), weight=1)
            for i, receita in enumerate(receitas):
                self.criar_card(self.scroll, receita, i)

    def criar_card(self, container, receita, indice):
        card = ctk.CTkFrame(container, fg_color=self.cor_card, corner_radius=15)
        card.grid(row=indice // 3, column=indice % 3, padx=10, pady=10, sticky="nsew")

        if receita.foto_path and os.path.exists(receita.foto_path):
            img_pil = Image.open(receita.foto_path)
            img_ctk = ctk.CTkImage(img_pil, size=(320, 180))
            ctk.CTkLabel(card, image=img_ctk, text="").pack(fill="x", side="top")
        else:
            p = ctk.CTkFrame(card, height=180, fg_color="#3D2B1F", corner_radius=15)
            p.pack(fill="x", side="top")
            ctk.CTkLabel(p, text="📸", font=("Arial", 40)).place(
                relx=0.5, rely=0.5, anchor="center"
            )

        ctk.CTkLabel(card, text=receita.nome, font=("Arial Bold", 18)).pack(
            anchor="w", padx=20, pady=(15, 2)
        )
        ctk.CTkLabel(
            card,
            text=f"⏱ {receita.tempo}",
            font=("Arial", 11),
            text_color=self.cor_laranja,
        ).pack(anchor="w", padx=20, pady=(0, 10))
        ctk.CTkButton(
            card,
            text="Ver Receita",
            fg_color="#38261A",
            hover_color="#4D3525",
            height=40,
            command=lambda i=indice: self.ver_receita(i),
        ).pack(fill="x", padx=20, pady=(5, 10))

        f_b = ctk.CTkFrame(card, fg_color="transparent")
        f_b.pack(fill="x", padx=20, pady=(0, 20))
        ctk.CTkButton(
            f_b,
            text="Editar",
            fg_color="transparent",
            border_width=1,
            border_color="#3D2B1F",
            height=35,
            command=lambda i=indice: self.editar_receita(i),
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ctk.CTkButton(
            f_b,
            text="🗑",
            fg_color="transparent",
            text_color="#E74C3C",
            width=40,
            command=lambda i=indice: self.remover_receita(i),
        ).pack(side="right")

    def ver_receita(self, indice):
        rec = self.livro.obter_receitas()[indice]
        self.limpar_tela()
        bg_cont = ctk.CTkFrame(self.root, fg_color="transparent")
        bg_cont.pack(fill="both", expand=True)
        cont = ctk.CTkFrame(bg_cont, fg_color="transparent", width=1000)
        cont.pack(pady=20, expand=True, fill="y")
        cont.pack_propagate(False)

        if rec.foto_path and os.path.exists(rec.foto_path):
            img = ctk.CTkImage(Image.open(rec.foto_path), size=(950, 380))
            banner = ctk.CTkLabel(cont, image=img, text="", corner_radius=20)
            banner.pack(pady=(0, 20))
            ctk.CTkLabel(
                banner,
                text=rec.nome,
                font=("Arial Bold", 40),
                text_color="white",
                fg_color="black",
            ).place(relx=0.05, rely=0.85, anchor="sw")

        info = ctk.CTkFrame(cont, fg_color="transparent")
        info.pack(fill="x", pady=10)
        for t, v, i in [("TEMPO", rec.tempo, "⏱"), ("PORÇÕES", rec.porcoes, "🍴")]:
            f = ctk.CTkFrame(
                info,
                fg_color=self.cor_card,
                height=85,
                corner_radius=15,
                border_width=1,
                border_color="#3D2B1F",
            )
            f.pack(side="left", expand=True, fill="x", padx=10)
            f.pack_propagate(False)
            ctk.CTkLabel(
                f, text=f"{i} {t}", font=("Arial Bold", 11), text_color=self.cor_laranja
            ).pack(pady=(15, 0), padx=25, anchor="w")
            ctk.CTkLabel(f, text=v, font=("Arial Bold", 20)).pack(
                pady=(0, 10), padx=25, anchor="w"
            )

        corpo = ctk.CTkFrame(cont, fg_color="transparent")
        corpo.pack(fill="both", expand=True, pady=20)
        col_i = ctk.CTkFrame(corpo, fg_color="transparent")
        col_i.pack(side="left", fill="both", expand=True, padx=(0, 30))
        ctk.CTkLabel(
            col_i,
            text="📝 Ingredientes",
            font=("Arial Bold", 22),
            text_color=self.cor_laranja,
        ).pack(anchor="w", pady=(0, 20))
        for ing in rec.ingredientes:
            ctk.CTkCheckBox(
                col_i,
                text=ing,
                font=("Arial", 15),
                fg_color=self.cor_laranja,
                border_color=self.cor_laranja,
            ).pack(anchor="w", pady=6)

        col_p = ctk.CTkFrame(corpo, fg_color="transparent")
        col_p.pack(side="right", fill="both", expand=True, padx=(30, 0))
        ctk.CTkLabel(
            col_p,
            text="🥣 Modo de Preparo",
            font=("Arial Bold", 22),
            text_color=self.cor_laranja,
        ).pack(anchor="w", pady=(0, 20))
        for i, p in enumerate(rec.modo_preparo):
            f = ctk.CTkFrame(col_p, fg_color="transparent")
            f.pack(fill="x", pady=12)
            ctk.CTkLabel(
                f,
                text=str(i + 1),
                font=("Arial Bold", 13),
                fg_color=self.cor_laranja,
                text_color="black",
                width=28,
                height=28,
                corner_radius=14,
            ).pack(side="left", padx=(0, 15), anchor="n")
            ctk.CTkLabel(
                f,
                text=p,
                font=("Arial", 15),
                wraplength=450,
                justify="left",
                anchor="w",
            ).pack(side="left", fill="x", expand=True)

        footer = ctk.CTkFrame(cont, fg_color="transparent")
        footer.pack(fill="x", pady=(50, 20), side="bottom")
        ctk.CTkButton(
            footer,
            text="← Voltar ao Dashboard",
            fg_color="#38261A",
            height=55,
            command=self.criar_tela_principal,
        ).pack(side="left", expand=True, fill="x", padx=(0, 15))
        ctk.CTkButton(
            footer,
            text="✎ Editar esta Receita",
            fg_color=self.cor_laranja,
            text_color="black",
            height=55,
            command=lambda: self.editar_receita(indice),
        ).pack(side="right", expand=True, fill="x", padx=(15, 0))

    def tela_adicionar(self):
        self.limpar_tela()
        self._exibir_formulario()

    def editar_receita(self, indice):
        rec = self.livro.obter_receitas()[indice]
        self.limpar_tela()
        self.foto_selecionada = rec.foto_path
        self._exibir_formulario(rec, indice)

    def _exibir_formulario(self, rec_ex=None, ind=None):
        form_wrap = ctk.CTkFrame(self.root, fg_color="transparent", width=800)
        form_wrap.pack(pady=20, expand=True, fill="y")
        scr = ctk.CTkScrollableFrame(
            form_wrap, fg_color="transparent", width=800, height=750
        )
        scr.pack(fill="both", expand=True)
        scr._scrollbar.grid_forget()

        ctk.CTkLabel(
            scr,
            text="Editar Receita" if rec_ex else "Nova Receita",
            font=("Arial Bold", 28),
        ).pack(pady=(0, 20))
        ctk.CTkLabel(
            scr,
            text="FOTO DA RECEITA",
            font=("Arial Bold", 13),
            text_color=self.cor_laranja,
        ).pack(anchor="w", pady=(10, 5))
        up = ctk.CTkFrame(
            scr,
            height=200,
            fg_color=self.cor_card,
            border_width=1,
            border_color=self.cor_texto_sec,
        )
        up.pack(fill="x", pady=5)
        up.pack_propagate(False)
        if rec_ex and rec_ex.foto_path and os.path.exists(rec_ex.foto_path):
            img = ctk.CTkImage(Image.open(rec_ex.foto_path), size=(700, 300))
            ctk.CTkLabel(up, image=img, text="").pack(expand=True, fill="both")
        ctk.CTkButton(
            up,
            text="📷 Toque para alterar",
            fg_color="transparent",
            command=lambda: self.selecionar_foto(up),
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            scr,
            text="NOME DA RECEITA",
            font=("Arial Bold", 13),
            text_color=self.cor_laranja,
        ).pack(anchor="w", pady=(20, 5))
        self.in_nome = ctk.CTkEntry(
            scr, placeholder_text="Ex: Lasanha", height=50, fg_color=self.cor_card
        )
        self.in_nome.pack(fill="x", pady=5)
        if rec_ex:
            self.in_nome.insert(0, rec_ex.nome)

        f_l = ctk.CTkFrame(scr, fg_color="transparent")
        f_l.pack(fill="x", pady=10)
        for t, var, val in [
            ("TEMPO DE PREPARO", "in_tempo", rec_ex.tempo if rec_ex else ""),
            ("PORÇÕES", "in_porcao", rec_ex.porcoes if rec_ex else ""),
        ]:
            f = ctk.CTkFrame(f_l, fg_color="transparent")
            f.pack(
                side="left" if "TEMPO" in t else "right", expand=True, fill="x", padx=5
            )
            ctk.CTkLabel(
                f, text=t, font=("Arial Bold", 13), text_color=self.cor_laranja
            ).pack(anchor="w")
            e = ctk.CTkEntry(
                f, placeholder_text="Ex: 45 min", height=45, fg_color=self.cor_card
            )
            e.pack(fill="x", pady=5)
            e.insert(0, val)
            setattr(self, var, e)

        ctk.CTkLabel(
            scr,
            text="INGREDIENTES",
            font=("Arial Bold", 13),
            text_color=self.cor_laranja,
        ).pack(anchor="w", pady=(10, 5))
        self.c_ing = ctk.CTkFrame(scr, fg_color="transparent")
        self.c_ing.pack(fill="x", pady=5)
        if rec_ex:
            for i in rec_ex.ingredientes:
                self.adicionar_campo_ingrediente(self.c_ing, i)
        else:
            self.adicionar_campo_ingrediente(self.c_ing)
        ctk.CTkButton(
            scr,
            text="+ Adicionar Ingrediente",
            fg_color="transparent",
            border_width=1,
            border_color="#3D2B1F",
            text_color=self.cor_laranja,
            command=lambda: self.adicionar_campo_ingrediente(self.c_ing),
        ).pack(fill="x", pady=10)

        ctk.CTkLabel(
            scr,
            text="MODO DE PREPARO",
            font=("Arial Bold", 13),
            text_color=self.cor_laranja,
        ).pack(anchor="w", pady=(10, 5))
        self.c_modo = ctk.CTkFrame(scr, fg_color="transparent")
        self.c_modo.pack(fill="x", pady=5)
        if rec_ex:
            for p in rec_ex.modo_preparo:
                self.adicionar_campo_modo(self.c_modo, p)
        else:
            self.adicionar_campo_modo(self.c_modo)
        ctk.CTkButton(
            scr,
            text="+ Adicionar Passo",
            fg_color="transparent",
            border_width=1,
            border_color="#3D2B1F",
            text_color=self.cor_laranja,
            command=lambda: self.adicionar_campo_modo(self.c_modo),
        ).pack(fill="x", pady=10)

        ctk.CTkButton(
            scr,
            text="Salvar Alterações" if rec_ex else "Salvar Receita",
            fg_color=self.cor_laranja,
            hover_color=self.cor_laranja_hover,
            text_color="black",
            font=("Arial Bold", 18),
            height=55,
            corner_radius=10,
            command=lambda: self.salvar_receita(ind),
        ).pack(fill="x", pady=30)
        ctk.CTkButton(
            scr,
            text="Voltar",
            fg_color="transparent",
            command=self.criar_tela_principal,
        ).pack()

    def salvar_receita(self, indice=None):
        i = [e.get() for e in self.entradas_ingredientes if e.get().strip()]
        p = [e.get() for e in self.entradas_modo if e.get().strip()]
        n = Receita(
            self.in_nome.get(),
            i,
            p,
            self.in_tempo.get(),
            self.in_porcao.get(),
            self.foto_selecionada,
        )
        if indice is not None:
            self.livro.obter_receitas()[indice] = n
        else:
            self.livro.adicionar_receita(n)
        self.criar_tela_principal()

    def remover_receita(self, indice):
        if messagebox.askyesno("Excluir", "Deseja remover esta receita?"):
            self.livro.remover_receita(indice)
            self.criar_tela_principal()

    def executar(self):
        self.root.mainloop()
