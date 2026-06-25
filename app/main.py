from fastapi import FastAPI, HTTPException, status
from typing import List
from modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from modelos.facturas import Factura, FacturaCrear, FacturaEditar
from modelos.transacciones import Transaccion, TransaccionCrear, TransaccionEditar

from app.enrutadores import clientes

app.include_router(clientes.rutas_clientes, tags=["clientes"])

app = FastAPI()

# Base de datos en memoria para cada modelo
lista_clientes: List[Cliente] = []
lista_facturas: List[Factura] = []
lista_transacciones: List[Transaccion] = []


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
    # Buscar cliente
    cliente_encontrado = None
    for cliente in lista_clientes:
        if cliente.id == cliente_id:
            cliente_encontrado = cliente
            break
    
    # Validar existencia
    if not cliente_encontrado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"El cliente con ID {cliente_id} no existe"
        )
    
    # Crear, validar, asignar cliente e ID, guardar
    factura_validada = Factura.model_validate(factura_crear.model_dump())
    factura_validada.cliente = cliente_encontrado
    factura_validada.id = len(lista_facturas) + 1
    
    lista_facturas.append(factura_validada)
    return factura_validada

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
async def crear_transaccion(factura_id: int, datos_transaccion: TransaccionCrear):
    # Lógica idéntica a la que el profesor escribe en el video
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
        
    # Validamos los datos enviándolos a diccionario
    transaccion_validada = Transaccion.model_validate(datos_transaccion.model_dump())
    
    # Generamos el ID automático
    transaccion_validada.id = len(lista_transacciones) + 1
    # Le asignamos a la transacción el ID de la factura que vino por la URL
    transaccion_validada.factura_id = factura_id
    
    # Agregamos la transacción validada a la lista interna de la factura encontrada
    factura_encontrada.transacciones.append(transaccion_validada)
    # También a la lista general de transacciones
    lista_transacciones.append(transaccion_validada)
    
    return transaccion_validada

# TAREA: EDITAR TRANSACCION (PATCH)
@app.patch("/transacciones/{transaccion_id}", response_model=Transaccion)
async def editar_transaccion(transaccion_id: int, datos_transaccion: TransaccionEditar):
    # Buscamos la transacción en la lista global
    for trans in lista_transacciones:
        if trans.id == transaccion_id:
            # Actualizamos sus datos
            trans.cantidad = datos_transaccion.cantidad
            trans.valor_unitario = datos_transaccion.valor_unitario
            return trans
    # Si termina el ciclo y no encuentra nada, lanzamos error
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transacción no encontrada")

# TAREA: ELIMINAR TRANSACCION (DELETE)
@app.delete("/transacciones/{transaccion_id}", response_model=Transaccion)
async def eliminar_transaccion(transaccion_id: int):
    # 1. Buscamos y eliminamos de la lista global
    for i, trans in enumerate(lista_transacciones):
        if trans.id == transaccion_id:
            transaccion_eliminada = lista_transacciones.pop(i)
            

            for factura in lista_facturas:
                factura.transacciones = [t for t in factura.transacciones if t.id != transaccion_id]
            
            return transaccion_eliminada
            
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transacción no encontrada")