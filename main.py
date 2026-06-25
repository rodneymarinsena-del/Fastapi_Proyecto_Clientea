from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from modelos.clientes import Cliente, ClienteCrear
from modelos.facturas import Factura, FacturaCrear
from modelos.transacciones import Transaccion, TransaccionCrear

app = FastAPI()

# Base de datos en memoria para cada modelo
lista_clientes: List[Cliente] = []
lista_facturas: List[Factura] = []
lista_transacciones: List[Transaccion] = []

# --- ENDPOINTS CLIENTES ---
@app.get("/clientes", response_model=List[Cliente])
def listar_clientes():
    return lista_clientes

@app.get("/clientes/{cliente_id}", response_model=Cliente)
def listar_cliente(cliente_id: int):
    for cliente in lista_clientes:
        if cliente.id == cliente_id:
            return cliente
    return {"mensaje": "Cliente no encontrado"}

@app.post("/clientes", response_model=Cliente)
def crear_cliente(cliente_crear: ClienteCrear):
    val = Cliente.model_validate(cliente_crear.model_dump())
    lista_clientes.append(val)
    return val

# --- ENDPOINTS FACTURAS ---
@app.get("/facturas", response_model=List[Factura])
def listar_facturas():
    return lista_facturas

@app.post("/facturas", response_model=Factura)
def crear_factura(factura_crear: FacturaCrear):
    val = Factura.model_validate(factura_crear.model_dump())
    lista_facturas.append(val)
    return val

# --- ENDPOINTS TRANSACCIONES ---
@app.get("/transacciones", response_model=List[Transaccion])
def listar_transacciones():
    return lista_transacciones

@app.post("/transacciones", response_model=Transaccion)
def crear_transaccion(transaccion_crear: TransaccionCrear):
    val = Transaccion.model_validate(transaccion_crear.model_dump())
    lista_transacciones.append(val)
    return val