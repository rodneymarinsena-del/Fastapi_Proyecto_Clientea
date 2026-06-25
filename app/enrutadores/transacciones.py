from fastapi import APIRouter, HTTPException, status
from typing import List
from app.modelos.transacciones import Transaccion, TransaccionCrear , TransaccionEditar
from app.listas import lista_transacciones, lista_facturas

rutas_transacciones = APIRouter()

@rutas_transacciones.get("/transacciones", response_model=List[Transaccion])
async def listar_transacciones():
    return lista_transacciones

@rutas_transacciones.post("/transacciones/{factura_id}", response_model=Transaccion)
async def crear_transaccion(factura_id: int, datos_transaccion: TransaccionCrear):
    factura_encontrada = None
    for factura in lista_facturas:
        if factura.id == factura_id:
            factura_encontrada = factura
            break
            
    if not factura_encontrada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"La factura con ID {factura_id} no existe"
        )
        
    transaccion_validada = Transaccion.model_validate(datos_transaccion.model_dump())
    transaccion_validada.id = len(lista_transacciones) + 1
    transaccion_validada.factura_id = factura_id
    
    factura_encontrada.transacciones.append(transaccion_validada)
    lista_transacciones.append(transaccion_validada)
    
    return transaccion_validada

@rutas_transacciones.patch("/transacciones/{transaccion_id}", response_model=Transaccion)
async def editar_transaccion(transaccion_id: int, datos_transaccion: TransaccionEditar):
    for i, objeto_transaccion in enumerate(lista_transacciones):
        if objeto_transaccion.id == transaccion_id:
            factura_id_actual = objeto_transaccion.factura_id
            
            val = Transaccion.model_validate(datos_transaccion.model_dump())
            val.id = transaccion_id
            val.factura_id = factura_id_actual
            
            # 1. Actualizar en la lista global de transacciones
            lista_transacciones[i] = val
            
            # 2. Sincronizar y actualizar dentro de la lista interna de la factura correspondiente
            for factura in lista_facturas:
                if factura.id == factura_id_actual:
                    for j, t_interna in enumerate(factura.transacciones):
                        if t_interna.id == transaccion_id:
                            factura.transacciones[j] = val
                            break
                    break
            return val
            
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail=f"La transacción con ID {transaccion_id} no existe"
    )

@rutas_transacciones.delete("/transacciones/{transaccion_id}", response_model=Transaccion)
async def eliminar_transaccion(transaccion_id: int):
    for i, objeto_transaccion in enumerate(lista_transacciones):
        if objeto_transaccion.id == transaccion_id:
            factura_id_actual = objeto_transaccion.factura_id
            transaccion_eliminada = lista_transacciones.pop(i)
            
            # Sincronizar y eliminar de la lista interna de la factura correspondiente
            for factura in lista_facturas:
                if factura.id == factura_id_actual:
                    for j, t_interna in enumerate(factura.transacciones):
                        if t_interna.id == transaccion_id:
                            factura.transacciones.pop(j)
                            break
                    break
            return transaccion_eliminada
            
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail=f"La transacción con ID {transaccion_id} no existe"
    )