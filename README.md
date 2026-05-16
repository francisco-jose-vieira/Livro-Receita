# 🍳 Diário de Receitas

Aplicativo desktop para gerenciar suas receitas favoritas, desenvolvido em **Python + CustomTkinter**, com arquitetura **MVC** clara e interface responsiva.

---

## 🗂 Estrutura do Projeto (MVC)

```
receitas_app/
│
├── main.py                         # Ponto de entrada
│
├── models/                         # MODEL — dados e regras de negócio
│   ├── receita.py                  # Entidade Receita (com checklist)
│   └── livro_receitas.py           # Coleção + PersistenciaJSON
│
├── views/                          # VIEW — interface gráfica (CustomTkinter)
│   ├── dashboard_view.py           # Grid de cards responsivo
│   ├── detalhes_view.py            # Detalhes + checklist de ingredientes
│   └── formulario_view.py          # Cadastro e edição de receitas
│
├── controllers/                    # CONTROLLER — mediador Model ↔ View
│   └── app_controller.py           # Navegação + ações do usuário
│
└── DB/
    └── receitas.json               # Gerado automaticamente
```

### Separação de responsabilidades

| Camada | O que faz | O que NÃO faz |
|---|---|---|
| **Model** | Armazena dados, persiste JSON | Nenhum widget, nenhuma lógica de tela |
| **View** | Renderiza widgets, emite eventos | Não acessa Model diretamente |
| **Controller** | Recebe eventos da View, atualiza Model, navega entre Views | Não cria widgets |

---

## ✨ Funcionalidades

- **CRUD completo** de receitas (nome, tempo, porções, foto, ingredientes, modo de preparo)
- **Checklist de ingredientes persistente** — o estado dos ingredientes marcados é salvo em disco e restaurado ao reabrir a receita
- **Barra de progresso** no checklist (ex: "3 de 7 ingredientes separados")
- **Botão Limpar** para resetar o checklist
- **Grid responsivo** — 3 colunas → 2 → 1 conforme a janela é redimensionada
- **Foto com preview** ao adicionar/editar
- **Validação** dos campos obrigatórios com alertas amigáveis
- **Persistência JSON** automática (pasta `DB/receitas.json`)

---

## 📦 Pré-requisitos

- Python 3.10+
- Git

---

## ⬇️ Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/francisco-jose-vieira/Livro-Receita.git
cd Livro-Receita

# 2. Instale as dependências
pip install customtkinter pillow

# 3. Execute
python main.py
```

---

## 👨‍💻 Stack

| Biblioteca | Uso |
|---|---|
| `customtkinter` | Interface gráfica moderna (dark mode nativo) |
| `Pillow` | Carregamento e redimensionamento de imagens |
| `json` + `os` | Persistência local (stdlib) |

---

## 📌 Observações

- O arquivo `DB/receitas.json` é criado automaticamente na primeira execução.
- O campo `checklist` dentro de cada receita no JSON guarda o estado de cada ingrediente marcado.
- A janela tem tamanho mínimo de **480×600 px** para garantir usabilidade em telas menores.
