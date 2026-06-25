from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List
from modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from modelos.facturas import Factura, FacturaCrear, FacturaEditar
from modelos.transacciones import Transaccion, TransaccionCrear, TransaccionEditar

app = FastAPI()

# Base de datos en memoria
lista_clientes: List[Cliente] = []
lista_facturas: List[Factura] = []
lista_transacciones: List[Transaccion] = []

# --- ENDPOINTS CLIENTES ---
@app.get("/clientes", response_model=List[Cliente])
async def listar_clientes():
    return lista_clientes

@app.get("/clientes/{cliente_id}", response_model=Cliente)
async def listar_cliente(cliente_id: int):
    for cliente in lista_clientes:
        if cliente.id == cliente_id:
            return cliente
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El cliente con ID {cliente_id} no existe")

@app.post("/clientes", response_model=Cliente)
async def crear_cliente(cliente_crear: ClienteCrear):
    id_cliente = len(lista_clientes) + 1
    val = Cliente.model_validate(cliente_crear.model_dump())
    val.id = id_cliente
    lista_clientes.append(val)
    return val

@app.patch("/clientes/{cliente_id}", response_model=Cliente)
async def editar_cliente(cliente_id: int, datos_cliente: ClienteEditar):
    for i, objeto_cliente in enumerate(lista_clientes):
        if objeto_cliente.id == cliente_id:
            val = Cliente.model_validate(datos_cliente.model_dump())
            val.id = cliente_id
            lista_clientes[i] = val
            return val
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El cliente con ID {cliente_id} no existe")

@app.delete("/clientes/{cliente_id}", response_model=Cliente)
async def eliminar_cliente(cliente_id: int):
    for i, objeto_cliente in enumerate(lista_clientes):
        if objeto_cliente.id == cliente_id:
            cliente_eliminado = lista_clientes.pop(i)
            return cliente_eliminado
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El cliente con ID {cliente_id} no existe")

# --- ENDPOINTS FACTURAS ---
@app.get("/facturas", response_model=List[Factura])
async def listar_facturas():
    return lista_facturas

@app.get("/facturas/{factura_id}", response_model=Factura)
async def listar_factura(factura_id: int):
    for factura in lista_facturas:
        if factura.id == factura_id:
            return factura
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"La factura con ID {factura_id} no existe")

@app.post("/facturas/{cliente_id}", response_model=Factura)
async def crear_factura(cliente_id: int, factura_crear: FacturaCrear):

    cliente_encontrado = None
    for cliente in lista_clientes:
        if cliente.id == cliente_id:
            cliente_encontrado = cliente
            break
    
    if not cliente_encontrado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"El cliente con ID {cliente_id} no existe, no se puede crear la factura"
        )
    
    id_factura = len(lista_facturas) + 1
    val = Factura.model_validate(factura_crear.model_dump())
    val.id = id_factura
    
    val.cliente = cliente_encontrado
    
   
    lista_facturas.append(val)
    return val

@app.patch("/facturas/{factura_id}", response_model=Factura)
async def editar_factura(factura_id: int, datos_factura: FacturaEditar):
    pass

@app.delete("/facturas/{factura_id}", response_model=Factura)
async def eliminar_factura(factura_id: int):
    pass

# --- ENDPOINTS TRANSACCIONES ---
@app.get("/transacciones", response_model=List[Transaccion])
async def listar_transacciones():
    return lista_transacciones

@app.get("/transacciones/{transaccion_id}", response_model=Transaccion)
async def listar_transaccion(transaccion_id: int):
    pass

@app.post("/transacciones/{factura_id}", response_model=Transaccion)
async def crear_transaccion(factura_id: int, transaccion_crear: TransaccionCrear):
    pass

@app.patch("/transacciones/{transaccion_id}", response_model=Transaccion)
async def editar_transaccion(transaccion_id: int, datos_transaccion: TransaccionEditar):
    pass

@app.delete("/transacciones/{transaccion_id}", response_model=Transaccion)
async def eliminar_transaccion(transaccion_id: int):
    pass