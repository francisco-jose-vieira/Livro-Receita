import customtkinter as ctk
from tkinter import Listbox, END, messagebox

from receita import Receita
from livro_receitas import LivroDeReceitas


class InterfaceReceitas:

    def __init__(self):

        self.livro = LivroDeReceitas()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Diário de Receitas")
        self.root.geometry("700x500")

        self.criar_tela_principal()


    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    def criar_tela_principal(self):

        self.limpar_tela()

        titulo = ctk.CTkLabel(self.root, text="📖 Diário de Receitas", font=("Arial", 24))
        titulo.pack(pady=20)

        self.lista = Listbox(self.root, height=10, font=("Arial", 12))
        self.lista.pack(fill="x", padx=40)

        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=20)

        ctk.CTkButton(frame, text="Adicionar Receita", command=self.tela_adicionar).grid(row=0, column=0, padx=10)

        ctk.CTkButton(frame, text="Ver Receita", command=self.ver_receita).grid(row=0, column=1, padx=10)

        ctk.CTkButton(frame, text="Editar Receita", command=self.editar_receita).grid(row=0, column=2, padx=10)

        ctk.CTkButton(frame, text="Remover Receita", command=self.remover_receita).grid(row=0, column=3, padx=10)

        self.atualizar_lista()


    def atualizar_lista(self):

        self.lista.delete(0, END)

        for receita in self.livro.obter_receitas():
            self.lista.insert(END, receita.nome)


    def obter_indice_selecionado(self):

        selecionado = self.lista.curselection()

        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma receita")
            return None

        return selecionado[0]


    def tela_adicionar(self):

        self.limpar_tela()

        titulo = ctk.CTkLabel(self.root, text="Nova Receita", font=("Arial", 22))
        titulo.pack(pady=10)

        self.nome = ctk.CTkEntry(self.root, placeholder_text="Nome da receita")
        self.nome.pack(fill="x", padx=40, pady=10)

        self.ingredientes = ctk.CTkTextbox(self.root, height=120)
        self.ingredientes.pack(fill="x", padx=40)
        self.ingredientes.insert("0.0", "Ingredientes (um por linha)")

        self.preparo = ctk.CTkTextbox(self.root, height=120)
        self.preparo.pack(fill="x", padx=40, pady=10)
        self.preparo.insert("0.0", "Modo de preparo (um passo por linha)")

        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10)

        ctk.CTkButton(frame, text="Salvar", command=self.salvar_receita).grid(row=0, column=0, padx=10)

        ctk.CTkButton(frame, text="Voltar", command=self.criar_tela_principal).grid(row=0, column=1, padx=10)


    def salvar_receita(self):

        nome = self.nome.get()

        ingredientes = self.ingredientes.get("1.0", "end").strip().split("\n")
        preparo = self.preparo.get("1.0", "end").strip().split("\n")

        receita = Receita(nome, ingredientes, preparo)

        self.livro.adicionar_receita(receita)

        self.criar_tela_principal()


    def ver_receita(self):

        indice = self.obter_indice_selecionado()

        if indice is None:
            return

        receita = self.livro.obter_receitas()[indice]

        self.limpar_tela()

        titulo = ctk.CTkLabel(self.root, text=receita.nome, font=("Arial", 24))
        titulo.pack(pady=20)

        texto = ctk.CTkTextbox(self.root)
        texto.pack(fill="both", expand=True, padx=40)

        texto.insert("0.0", receita.texto_receita())

        texto.configure(state="disabled")

        ctk.CTkButton(self.root, text="Voltar", command=self.criar_tela_principal).pack(pady=20)


    def remover_receita(self):

        indice = self.obter_indice_selecionado()

        if indice is None:
            return

        self.livro.remover_receita(indice)

        self.atualizar_lista()


    def editar_receita(self):

        indice = self.obter_indice_selecionado()

        if indice is None:
            return

        receita = self.livro.obter_receitas()[indice]

        self.limpar_tela()

        titulo = ctk.CTkLabel(self.root, text="Editar Receita", font=("Arial", 22))
        titulo.pack(pady=10)

        self.nome = ctk.CTkEntry(self.root)
        self.nome.pack(fill="x", padx=40, pady=10)
        self.nome.insert(0, receita.nome)

        self.ingredientes = ctk.CTkTextbox(self.root, height=120)
        self.ingredientes.pack(fill="x", padx=40)

        self.ingredientes.insert("0.0", "\n".join(receita.ingredientes))

        self.preparo = ctk.CTkTextbox(self.root, height=120)
        self.preparo.pack(fill="x", padx=40, pady=10)

        self.preparo.insert("0.0", "\n".join(receita.modo_preparo))

        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10)

        def salvar_edicao():

            receita.nome = self.nome.get()
            receita.ingredientes = self.ingredientes.get("1.0", "end").strip().split("\n")
            receita.modo_preparo = self.preparo.get("1.0", "end").strip().split("\n")

            self.criar_tela_principal()

        ctk.CTkButton(frame, text="Salvar Alterações", command=salvar_edicao).grid(row=0, column=0, padx=10)

        ctk.CTkButton(frame, text="Voltar", command=self.criar_tela_principal).grid(row=0, column=1, padx=10)


    def executar(self):
        self.root.mainloop()