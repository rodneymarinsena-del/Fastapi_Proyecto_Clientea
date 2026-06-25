from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlmodel import Session, select
from app.modelos.facturas import Factura, FacturaCrear, FacturaEditar
from app.modelos.clientes import Cliente
from app.database import get_session

rutas_facturas = APIRouter()

# --- ENDPOINTS FACTURAS ---

@rutas_facturas.get("/facturas", response_model=List[Factura])
def listar_facturas(session: Session = Depends(get_session)):
    facturas = session.exec(select(Factura)).all()
    return facturas

@rutas_facturas.get("/facturas/{factura_id}", response_model=Factura)
def listar_factura(factura_id: int, session: Session = Depends(get_session)):
    factura = session.get(Factura, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura

@rutas_facturas.post("/facturas/{cliente_id}", response_model=Factura)
def crear_factura(cliente_id: int, factura_crear: FacturaCrear, session: Session = Depends(get_session)):
    # Verificamos que el cliente exista en la BD
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Creamos la factura vinculada al cliente
    nueva_factura = Factura.model_validate(factura_crear.model_dump())
    nueva_factura.cliente_id = cliente_id 
    
    session.add(nueva_factura)
    session.commit()
    session.refresh(nueva_factura)
    return nueva_factura

@rutas_facturas.patch("/facturas/{factura_id}", response_model=Factura)
def editar_factura(factura_id: int, datos_factura: FacturaEditar, session: Session = Depends(get_session)):
    factura = session.get(Factura, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    datos_dict = datos_factura.model_dump(exclude_unset=True)
    factura.sqlmodel_update(datos_dict)
    
    session.add(factura)
    session.commit()
    session.refresh(factura)
    return factura

@rutas_facturas.delete("/facturas/{factura_id}")
def eliminar_factura(factura_id: int, session: Session = Depends(get_session)):
    factura = session.get(Factura, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    session.delete(factura)
    session.commit()
    return {"message": "Factura eliminada con éxito"}