from fastapi import APIRouter, HTTPException, status
from typing import List
from app.modelos.facturas import Factura, FacturaCrear, FacturaEditar
from app.listas import lista_facturas, lista_clientes

rutas_facturas = APIRouter()

@rutas_facturas.get("/facturas", response_model=List[Factura])
async def listar_facturas():
    return lista_facturas

@rutas_facturas.get("/facturas/{factura_id}", response_model=Factura)
async def listar_factura(factura_id: int):
    for factura in lista_facturas:
        if factura.id == factura_id:
            return factura
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"La factura con ID {factura_id} no existe")

@rutas_facturas.post("/facturas/{cliente_id}", response_model=Factura)
async def crear_factura(cliente_id: int, factura_crear: FacturaCrear):
    cliente_encontrado = None
    for cliente in lista_clientes:
        if cliente.id == cliente_id:
            cliente_encontrado = cliente
            break
    
    if not cliente_encontrado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"El cliente con ID {cliente_id} no existe"
        )
    
    factura_validada = Factura.model_validate(factura_crear.model_dump())
    factura_validada.cliente = cliente_encontrado
    factura_validada.id = len(lista_facturas) + 1
    
    lista_facturas.append(factura_validada)
    return factura_validada 

@rutas_facturas.patch("/facturas/{factura_id}", response_model=Factura)
async def editar_factura(factura_id: int, datos_factura: FacturaEditar):
    for i, objeto_factura in enumerate(lista_facturas):
        if objeto_factura.id == factura_id:
            # Conservamos los datos relacionales existentes que no cambian en la edición básica
            cliente_actual = objeto_factura.cliente
            transacciones_actuales = objeto_factura.transacciones
            
            val = Factura.model_validate(datos_factura.model_dump())
            val.id = factura_id
            val.cliente = cliente_actual
            val.transacciones = transacciones_actuales
            
            lista_facturas[i] = val
            return val
            
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail=f"La factura con ID {factura_id} no existe"
    )

@rutas_facturas.delete("/facturas/{factura_id}", response_model=Factura)
async def eliminar_factura(factura_id: int):
    for i, objeto_factura in enumerate(lista_facturas):
        if objeto_factura.id == factura_id:
            factura_eliminada = lista_facturas.pop(i)
            return factura_eliminada
            
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail=f"La factura con ID {factura_id} no existe"
    )
