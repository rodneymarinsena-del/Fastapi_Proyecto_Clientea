from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo del Cliente
class Cliente(BaseModel):
    id: int
    nombre: str
    email: str
    descripcion: str

# Base de datos en memoria
lista_clientes: List[Cliente] = []

# Endpoint: Listar todos
@app.get("/clientes")
def listar_clientes():
    return lista_clientes

# Endpoint: Listar uno solo
@app.get("/clientes/{cliente_id}")
def listar_cliente(cliente_id: int):
    for cliente in lista_clientes:
        if cliente.id == cliente_id:
            return cliente
    return {"mensaje": "Cliente no encontrado"}

# Endpoint: Crear cliente
@app.post("/clientes")
def crear_cliente(cliente: Cliente):
    lista_clientes.append(cliente)
    return cliente