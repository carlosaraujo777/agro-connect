from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Permite que o Front-end acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- BANCO DE DADOS (SQLite) ---
def criar_banco():
    conn = sqlite3.connect('agroconnect.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            custo REAL,
            quantidade INTEGER
        )
    ''')
    conn.commit()
    conn.close()

criar_banco()

# --- MODELOS (O que a API espera receber) ---
class Produto(BaseModel):
    nome: str
    custo: float
    quantidade: int

# --- ROTAS ---

@app.get("/")
def home():
    return {"status": "AgroConnect Online"}

# Rota pra listar os produtos (GET)
@app.get("/api/produtos")
def listar_produtos():
    conn = sqlite3.connect('agroconnect.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    dados = cursor.fetchall()
    conn.close()
    
    # Converte os dados pro formato JSON
    produtos = [{"id": d[0], "nome": d[1], "custo": d[2], "quantidade": d[3]} for d in dados]
    return produtos

# Rota pra adicionar um produto (POST)
@app.post("/api/produtos")
def adicionar_produto(produto: Produto):
    # Valida se o nome não tá vazio e se os números são maiores que zero
    if not produto.nome or produto.custo <= 0 or produto.quantidade <= 0:
        return {"erro": "Preencha todos os campos corretamente!"}
    
    conn = sqlite3.connect('agroconnect.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, custo, quantidade) VALUES (?, ?, ?)",
        (produto.nome, produto.custo, produto.quantidade)
    )
    conn.commit()
    conn.close()
    return {"mensagem": "Produto cadastrado com sucesso!"}

# Rota pra buscar a cotação da saca (GET)
@app.get("/api/cotacao/{produto}")
def buscar_cotacao(produto: str):
    # Simulando o preço da saca de soja no mercado atual
    if produto.lower() == 'soja':
        preco_saca = 135.00
    elif produto.lower() == 'milho':
        preco_saca = 65.00
    else:
        preco_saca = 100.00
    
    return {"produto": produto, "preco_saca": preco_saca}