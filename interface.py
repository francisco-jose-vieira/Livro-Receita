import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont
import os

from receita import Receita
from livro_receitas import LivroDeReceitas

# =========================================================
# CLASSE 1: DashboardView (A tela principal com os cards)
# =========================================================
class DashboardView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller

    def renderizar(self, receitas):
        self.container = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.container.pack(pady=20, expand=True, fill="both")

        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", padx=60, pady=(40, 10))

        info_f = ctk.CTkFrame(header, fg_color="transparent")
        info_f.pack(side="left")
        ctk.CTkLabel(info_f, text="Minhas Receitas", font=("Arial Bold", 32)).pack(anchor="w")
        ctk.CTkLabel(info_f, text="Gerencie suas criações favoritas", font=("Arial", 14), text_color="#8D7B6D").pack(anchor="w")

        ctk.CTkButton(header, text="+ Adicionar Receita", fg_color="#F5912E", hover_color="#FFB066",
                      text_color="black", font=("Arial Bold", 15), height=45, corner_radius=10, 
                      command=self.controller.tela_adicionar).pack(side="right")

        if not receitas:
            ctk.CTkLabel(self.container, text="Nenhuma receita encontrada.", font=("Arial", 18, "italic"), text_color="#8D7B6D").place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent", width=1000, height=650)
            self.scroll.pack(fill="both", expand=True, padx=50, pady=20)
            self.scroll.grid_columnconfigure((0, 1, 2), weight=1)
            for i, receita in enumerate(receitas):
                self.criar_card(self.scroll, receita, i)

    def criar_card(self, container, receita, indice):
        card = ctk.CTkFrame(container, fg_color="#24170E", corner_radius=15)
        card.grid(row=indice // 3, column=indice % 3, padx=10, pady=10, sticky="nsew")

        if receita.foto_path and os.path.exists(receita.foto_path):
            img_pil = Image.open(receita.foto_path)
            img_ctk = ctk.CTkImage(img_pil, size=(320, 180))
            ctk.CTkLabel(card, image=img_ctk, text="").pack(fill="x", side="top")
        else:
            p = ctk.CTkFrame(card, height=180, fg_color="#3D2B1F", corner_radius=15)
            p.pack(fill="x", side="top")
            ctk.CTkLabel(p, text="📸", font=("Arial", 40)).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text=receita.nome, font=("Arial Bold", 18)).pack(anchor="w", padx=20, pady=(15, 2))
        ctk.CTkLabel(card, text=f"⏱ {receita.tempo}  |  🍴 {receita.porcoes}", font=("Arial", 11), text_color="#F5912E").pack(anchor="w", padx=20, pady=(0, 10))
        
        ctk.CTkButton(card, text="Ver Receita", fg_color="#38261A", hover_color="#4D3525", height=40, 
                      command=lambda i=indice: self.controller.ver_receita(i)).pack(fill="x", padx=20, pady=(5, 10))

        f_b = ctk.CTkFrame(card, fg_color="transparent")
        f_b.pack(fill="x", padx=20, pady=(0, 20))
        ctk.CTkButton(f_b, text="Editar", fg_color="transparent", border_width=1, border_color="#3D2B1F", height=35, 
                      command=lambda i=indice: self.controller.editar_receita(i)).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ctk.CTkButton(f_b, text="🗑", fg_color="transparent", text_color="#E74C3C", width=40, 
                      command=lambda i=indice: self.controller.remover_receita(i)).pack(side="right")

# =========================================================
# CLASSE 2: VisualizadorDetalhes (Exibição da receita)
# =========================================================
class VisualizadorDetalhes:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller

    def renderizar(self, rec, indice):
        self.container = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        
        scr = ctk.CTkScrollableFrame(self.container, fg_color="transparent", width=1000, height=850)
        scr.pack(pady=20, expand=True, fill="y")

        if rec.foto_path and os.path.exists(rec.foto_path):
            img = ctk.CTkImage(Image.open(rec.foto_path), size=(950, 380))
            banner = ctk.CTkLabel(scr, image=img, text="", corner_radius=20)
            banner.pack(pady=(0, 20))
            ctk.CTkLabel(banner, text=rec.nome, font=("Arial Bold", 40), text_color="white", fg_color="black").place(relx=0.05, rely=0.85, anchor="sw")
        else:
            ctk.CTkLabel(scr, text=rec.nome, font=("Arial Bold", 35), text_color="#F5912E").pack(pady=20)

        info = ctk.CTkFrame(scr, fg_color="transparent")
        info.pack(fill="x", pady=10)
        for t, v, i in [("TEMPO", rec.tempo, "⏱"), ("PORÇÕES", rec.porcoes, "🍴")]:
            f = ctk.CTkFrame(info, fg_color="#24170E", height=85, corner_radius=15, border_width=1, border_color="#3D2B1F")
            f.pack(side="left", expand=True, fill="x", padx=10)
            f.pack_propagate(False)
            ctk.CTkLabel(f, text=f"{i} {t}", font=("Arial Bold", 11), text_color="#F5912E").pack(pady=(15, 0), padx=25, anchor="w")
            ctk.CTkLabel(f, text=v, font=("Arial Bold", 20)).pack(pady=(0, 10), padx=25, anchor="w")

        corpo = ctk.CTkFrame(scr, fg_color="transparent")
        corpo.pack(fill="both", expand=True, pady=20)
        
        col_i = ctk.CTkFrame(corpo, fg_color="transparent")
        col_i.pack(side="left", fill="both", expand=True, padx=(0, 30))
        ctk.CTkLabel(col_i, text="📝 Ingredientes", font=("Arial Bold", 22), text_color="#F5912E").pack(anchor="w", pady=(0, 20))
        for ing in rec.ingredientes:
            ctk.CTkCheckBox(col_i, text=ing, font=("Arial", 15), fg_color="#F5912E", border_color="#F5912E").pack(anchor="w", pady=6)

        col_p = ctk.CTkFrame(corpo, fg_color="transparent")
        col_p.pack(side="right", fill="both", expand=True, padx=(30, 0))
        ctk.CTkLabel(col_p, text="🥣 Modo de Preparo", font=("Arial Bold", 22), text_color="#F5912E").pack(anchor="w", pady=(0, 20))
        for i, p in enumerate(rec.modo_preparo):
            f = ctk.CTkFrame(col_p, fg_color="transparent")
            f.pack(fill="x", pady=12)
            ctk.CTkLabel(f, text=str(i + 1), font=("Arial Bold", 13), fg_color="#F5912E", text_color="black", width=28, height=28, corner_radius=14).pack(side="left", padx=(0, 15), anchor="n")
            ctk.CTkLabel(f, text=p, font=("Arial", 15), wraplength=450, justify="left", anchor="w").pack(side="left", fill="x", expand=True)

        footer = ctk.CTkFrame(scr, fg_color="transparent")
        footer.pack(fill="x", pady=(50, 20))
        ctk.CTkButton(footer, text="← Voltar", fg_color="#38261A", height=55, command=self.controller.criar_tela_principal).pack(side="left", expand=True, fill="x", padx=(0, 15))
        ctk.CTkButton(footer, text="✎ Editar", fg_color="#F5912E", text_color="black", height=55, command=lambda: self.controller.editar_receita(indice)).pack(side="right", expand=True, fill="x", padx=(15, 0))

# =========================================================
# CLASSE 3: FormularioView (A tela de cadastro/edição)
# =========================================================
class FormularioView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.entradas_ingredientes = []
        self.entradas_modo = []

    def renderizar(self, rec_ex=None, ind=None):
        self.entradas_ingredientes = []; self.entradas_modo = []
        form_wrap = ctk.CTkFrame(self.parent, fg_color="transparent")
        form_wrap.pack(pady=20, expand=True, fill="y")
        self.scr = ctk.CTkScrollableFrame(form_wrap, fg_color="transparent", width=800, height=750)
        self.scr.pack(fill="both", expand=True)

        ctk.CTkLabel(self.scr, text="Nova Receita" if not rec_ex else "Editar Receita", font=("Arial Bold", 28)).pack(pady=(0, 20))

        self.up = ctk.CTkFrame(self.scr, height=200, fg_color="#24170E", border_width=1, border_color="#8D7B6D")
        self.up.pack(fill="x", pady=5); self.up.pack_propagate(False)
        
        if rec_ex and rec_ex.foto_path and os.path.exists(rec_ex.foto_path):
            img = ctk.CTkImage(Image.open(rec_ex.foto_path), size=(700, 300))
            ctk.CTkLabel(self.up, image=img, text="").pack(expand=True, fill="both")
        
        ctk.CTkButton(self.up, text="📷 Alterar Foto", fg_color="transparent", command=self.controller.selecionar_foto).place(relx=0.5, rely=0.5, anchor="center")

        self.in_nome = ctk.CTkEntry(self.scr, placeholder_text="Nome da Receita", height=50, fg_color="#24170E", border_color="#3D2B1F")
        self.in_nome.pack(fill="x", pady=10)
        if rec_ex: self.in_nome.insert(0, rec_ex.nome)

        f_l = ctk.CTkFrame(self.scr, fg_color="transparent"); f_l.pack(fill="x", pady=10)
        
        # Tempo
        f_t = ctk.CTkFrame(f_l, fg_color="transparent"); f_t.pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkLabel(f_t, text="TEMPO (apenas número)", font=("Arial Bold", 13), text_color="#F5912E").pack(anchor="w")
        self.in_tempo = ctk.CTkEntry(f_t, placeholder_text="Ex: 45", height=45, fg_color="#24170E", border_color="#3D2B1F")
        self.in_tempo.pack(fill="x", pady=5)
        if rec_ex: self.in_tempo.insert(0, rec_ex.tempo.replace(" min", ""))

        # Porções
        f_p = ctk.CTkFrame(f_l, fg_color="transparent"); f_p.pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkLabel(f_p, text="PORÇÕES (apenas número)", font=("Arial Bold", 13), text_color="#F5912E").pack(anchor="w")
        self.in_porcao = ctk.CTkEntry(f_p, placeholder_text="Ex: 4", height=45, fg_color="#24170E", border_color="#3D2B1F")
        self.in_porcao.pack(fill="x", pady=5)
        if rec_ex: self.in_porcao.insert(0, rec_ex.porcoes.replace(" porções", ""))

        # Ingredientes
        self.c_ing = ctk.CTkFrame(self.scr, fg_color="transparent"); self.c_ing.pack(fill="x")
        if rec_ex: 
            for i in rec_ex.ingredientes: self.add_campo(self.c_ing, self.entradas_ingredientes, "ing", i)
        else: self.add_campo(self.c_ing, self.entradas_ingredientes, "ing")
        ctk.CTkButton(self.scr, text="+ Ingrediente", text_color="#F5912E", fg_color="transparent", border_width=1, border_color="#3D2B1F", 
                      command=lambda: self.add_campo(self.c_ing, self.entradas_ingredientes, "ing")).pack(fill="x", pady=10)

        # Modo
        self.c_modo = ctk.CTkFrame(self.scr, fg_color="transparent"); self.c_modo.pack(fill="x")
        if rec_ex:
            for p in rec_ex.modo_preparo: self.add_campo(self.c_modo, self.entradas_modo, "modo", p)
        else: self.add_campo(self.c_modo, self.entradas_modo, "modo")
        ctk.CTkButton(self.scr, text="+ Passo", text_color="#F5912E", fg_color="transparent", border_width=1, border_color="#3D2B1F", 
                      command=lambda: self.add_campo(self.c_modo, self.entradas_modo, "modo")).pack(fill="x", pady=10)

        ctk.CTkButton(self.scr, text="Salvar", fg_color="#F5912E", text_color="black", font=("Arial Bold", 18), height=55, 
                      command=lambda: self.controller.salvar_receita(ind)).pack(fill="x", pady=30)
        ctk.CTkButton(self.scr, text="Cancelar", fg_color="transparent", text_color="#8D7B6D", command=self.controller.criar_tela_principal).pack()

    def add_campo(self, container, lista, tipo, texto=""):
        frame = ctk.CTkFrame(container, fg_color="transparent"); frame.pack(fill="x", pady=5)
        lbl = ctk.CTkLabel(frame, text=f"{len(lista)+1}.", font=("Arial Bold", 14), text_color="#F5912E")
        lbl.pack(side="left", padx=(0, 10))
        
        e = ctk.CTkEntry(frame, height=45, fg_color="#24170E", border_color="#3D2B1F", 
                         placeholder_text="Ex: 500g de farinha" if tipo=="ing" else "Ex: Bata as claras...")
        e.insert(0, texto); e.pack(side="left", fill="x", expand=True)
        lista.append(e)
        
        ctk.CTkButton(frame, text="🗑", width=40, height=45, fg_color="transparent", text_color="#E74C3C", 
                      command=lambda: self.remover_campo(frame, e, lista, container)).pack(side="right", padx=(10, 0))

    def remover_campo(self, frame, entrada, lista, container):
        lista.remove(entrada)
        frame.destroy()
        # Atualiza a numeração
        for i, child in enumerate(container.winfo_children()):
            for sub in child.winfo_children():
                if isinstance(sub, ctk.CTkLabel):
                    sub.configure(text=f"{i+1}.")
                    break

# =========================================================
# CLASSE 4: InterfaceReceitas (O AppController/Cérebro)
# =========================================================
class InterfaceReceitas:
    def __init__(self):
        self.livro = LivroDeReceitas()
        self.root = ctk.CTk()
        self.root.title("Diário de Receitas")
        self.root.geometry("1150x900")
        self.root.configure(fg_color="#1A120B")
        
        # Estado temporário da foto
        self.foto_temporaria = None

        # Instancia as Views
        self.dash_view = DashboardView(self.root, self)
        self.form_view = FormularioView(self.root, self)
        self.detalhe_view = VisualizadorDetalhes(self.root, self)

        self.criar_tela_principal()

    def limpar_tela(self):
        for widget in self.root.winfo_children(): widget.pack_forget()

    def criar_tela_principal(self):
        self.limpar_tela()
        self.dash_view.renderizar(self.livro.obter_receitas())

    def tela_adicionar(self):
        self.limpar_tela()
        self.foto_temporaria = None
        self.form_view.renderizar()

    def editar_receita(self, indice):
        self.limpar_tela()
        rec = self.livro.obter_receitas()[indice]
        self.foto_temporaria = rec.foto_path
        self.form_view.renderizar(rec, indice)

    def ver_receita(self, indice):
        self.limpar_tela()
        rec = self.livro.obter_receitas()[indice]
        self.detalhe_view.renderizar(rec, indice)

    def selecionar_foto(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.png *.jpeg")])
        if caminho:
            self.foto_temporaria = caminho
            # Atualiza a prévia na view do formulário
            for widget in self.form_view.up.winfo_children(): widget.destroy()
            img_pil = Image.open(caminho)
            img_pil.thumbnail((700, 300))
            img_ctk = ctk.CTkImage(img_pil, size=img_pil.size)
            ctk.CTkLabel(self.form_view.up, image=img_ctk, text="").pack(expand=True, fill="both")

    def salvar_receita(self, indice=None):
        f = self.form_view
        nova = Receita(f.in_nome.get(), [e.get() for e in f.entradas_ingredientes if e.get()],
                       [e.get() for e in f.entradas_modo if e.get()], 
                       f"{f.in_tempo.get()} min", f"{f.in_porcao.get()} porções", self.foto_temporaria)
        
        if indice is not None:
            self.livro.receitas[indice] = nova
            self.livro.persistencia.salvar(self.livro.receitas)
        else:
            self.livro.adicionar_receita(nova)
        self.criar_tela_principal()

    def remover_receita(self, indice):
        if messagebox.askyesno("Excluir", "Deseja remover esta receita?"):
            self.livro.remover_receita(indice)
            self.criar_tela_principal()

    def executar(self):
        self.root.mainloop()