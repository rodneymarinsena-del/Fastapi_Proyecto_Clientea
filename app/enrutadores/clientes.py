from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlmodel import Session, select
from app.modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from app.database import get_session # Importamos la dependencia

rutas_clientes = APIRouter()

# --- ENDPOINTS CLIENTES ---

@rutas_clientes.get("/clientes", response_model=List[Cliente])
def listar_clientes(session: Session = Depends(get_session)):
    clientes = session.exec(select(Cliente)).all()
    return clientes

@rutas_clientes.get("/clientes/{cliente_id}", response_model=Cliente)
def listar_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@rutas_clientes.post("/clientes", response_model=Cliente)
def crear_cliente(cliente_crear: ClienteCrear, session: Session = Depends(get_session)):
    # Convertimos el modelo de creación a un objeto Cliente (de base de datos)
    nuevo_cliente = Cliente.model_validate(cliente_crear.model_dump())
    session.add(nuevo_cliente)
    session.commit()
    session.refresh(nuevo_cliente)
    return nuevo_cliente

@rutas_clientes.patch("/clientes/{cliente_id}", response_model=Cliente)
def editar_cliente(cliente_id: int, datos_cliente: ClienteEditar, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Actualizamos los datos
    datos_dict = datos_cliente.model_dump(exclude_unset=True)
    for key, value in datos_dict.items():
        setattr(cliente, key, value)
    
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente

@rutas_clientes.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    session.delete(cliente)
    session.commit()
    return {"message": "Cliente eliminado con éxito"}