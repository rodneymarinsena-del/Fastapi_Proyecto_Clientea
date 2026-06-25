from fastapi import APIRouter, HTTPException, status
from typing import List
from app.modelos.clientes import Cliente, ClienteCrear, ClienteEditar

# Instanciamos el router
rutas_clientes = APIRouter()


lista_clientes: List[Cliente] = []

# --- ENDPOINTS CLIENTES ---
@rutas_clientes.get("/clientes", response_model=List[Cliente])
async def listar_clientes():
    return lista_clientes

@rutas_clientes.get("/clientes/{cliente_id}", response_model=Cliente)
async def listar_cliente(cliente_id: int):
    for cliente in lista_clientes:
        if cliente.id == cliente_id:
            return cliente
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El cliente con ID {cliente_id} no existe")

@rutas_clientes.post("/clientes", response_model=Cliente)
async def crear_cliente(cliente_crear: ClienteCrear):
    id_cliente = len(lista_clientes) + 1
    val = Cliente.model_validate(cliente_crear.model_dump())
    val.id = id_cliente
    lista_clientes.append(val)
    return val

@rutas_clientes.patch("/clientes/{cliente_id}", response_model=Cliente)
async def editar_cliente(cliente_id: int, datos_cliente: ClienteEditar):
    for i, objeto_cliente in enumerate(lista_clientes):
        if objeto_cliente.id == cliente_id:
            val = Cliente.model_validate(datos_cliente.model_dump())
            val.id = cliente_id
            lista_clientes[i] = val
            return val
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El cliente con ID {cliente_id} no existe")

@rutas_clientes.delete("/clientes/{cliente_id}", response_model=Cliente)
async def eliminar_cliente(cliente_id: int):
    for i, objeto_cliente in enumerate(lista_clientes):
        if objeto_cliente.id == cliente_id:
            cliente_eliminado = lista_clientes.pop(i)
            return cliente_eliminado
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El cliente con ID {cliente_id} no existe")