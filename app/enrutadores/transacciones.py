from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlmodel import Session, select
from app.modelos.transacciones import Transaccion, TransaccionCrear, TransaccionEditar
from app.modelos.facturas import Factura
from app.database import get_session

rutas_transacciones = APIRouter()

# --- ENDPOINTS TRANSACCIONES ---

@rutas_transacciones.get("/transacciones", response_model=List[Transaccion])
def listar_transacciones(session: Session = Depends(get_session)):
    transacciones = session.exec(select(Transaccion)).all()
    return transacciones

@rutas_transacciones.post("/transacciones/{factura_id}", response_model=Transaccion)
def crear_transaccion(factura_id: int, datos_transaccion: TransaccionCrear, session: Session = Depends(get_session)):
    # 1. Verificamos que la factura exista
    factura = session.get(Factura, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    # 2. Creamos la transacción vinculada a la factura
    nueva_transaccion = Transaccion.model_validate(datos_transaccion.model_dump())
    nueva_transaccion.factura_id = factura_id
    
    session.add(nueva_transaccion)
    session.commit()
    session.refresh(nueva_transaccion)
    return nueva_transaccion

@rutas_transacciones.patch("/transacciones/{transaccion_id}", response_model=Transaccion)
def editar_transaccion(transaccion_id: int, datos_transaccion: TransaccionEditar, session: Session = Depends(get_session)):
    transaccion = session.get(Transaccion, transaccion_id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    # Usamos sqlmodel_update para un código más profesional
    datos_dict = datos_transaccion.model_dump(exclude_unset=True)
    transaccion.sqlmodel_update(datos_dict)
        
    session.add(transaccion)
    session.commit()
    session.refresh(transaccion)
    return transaccion

@rutas_transacciones.delete("/transacciones/{transaccion_id}")
def eliminar_transaccion(transaccion_id: int, session: Session = Depends(get_session)):
    transaccion = session.get(Transaccion, transaccion_id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    session.delete(transaccion)
    session.commit()
    return {"message": "Transacción eliminada con éxito"}