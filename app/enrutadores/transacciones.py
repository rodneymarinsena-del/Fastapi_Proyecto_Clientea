from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlmodel import Session, select
from app.modelos.transacciones import (
    Transaccion, 
    TransaccionCrear, 
    TransaccionEditar, 
    TransaccionLeer
)
from app.database import get_session

rutas_transacciones = APIRouter()

# --- ENDPOINTS TRANSACCIONES ---

@rutas_transacciones.get("/transacciones", response_model=List[TransaccionLeer])
def listar_transacciones(session: Session = Depends(get_session)):
    transacciones = session.exec(select(Transaccion)).all()
    return transacciones

@rutas_transacciones.post("/facturas/{factura_id}/transacciones", response_model=TransaccionLeer)
def crear_transaccion(factura_id: int, transaccion_data: TransaccionCrear, session: Session = Depends(get_session)):
    
    # 1. Importación Lazy para evitar error de importación circular
    from app.modelos.facturas import Factura
    
    # 2. Verificar existencia
    factura = session.get(Factura, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail=f"No existe una factura con ID {factura_id}")
    
    # 3. La corrección: Usamos 'update' para inyectar el factura_id durante la validación
    transaccion_db = Transaccion.model_validate(
        transaccion_data, 
        update={"factura_id": factura_id}
    )
    
    # 4. Guardar
    try:
        session.add(transaccion_db)
        session.commit()
        session.refresh(transaccion_db)
        return transaccion_db
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@rutas_transacciones.patch("/transacciones/{transaccion_id}", response_model=TransaccionLeer)
def editar_transaccion(transaccion_id: int, datos_transaccion: TransaccionEditar, session: Session = Depends(get_session)):
    transaccion = session.get(Transaccion, transaccion_id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
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