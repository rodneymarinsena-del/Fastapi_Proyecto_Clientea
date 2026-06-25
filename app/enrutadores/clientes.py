from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.modelos.clientes import Cliente, ClienteCrear, ClienteEditar

rutas_clientes = APIRouter()

# 1. Crear
@rutas_clientes.post("/clientes/", response_model=Cliente)
def crear_cliente(cliente_datos: ClienteCrear, session: Session = Depends(get_session)):
    cliente_db = Cliente.model_validate(cliente_datos)
    session.add(cliente_db)
    session.commit()
    session.refresh(cliente_db)
    return cliente_db

# 2. Listar
@rutas_clientes.get("/clientes/", response_model=List[Cliente])
def listar_clientes(session: Session = Depends(get_session)):
    clientes = session.exec(select(Cliente)).all()
    return clientes

# 3. Obtener uno
@rutas_clientes.get("/clientes/{cliente_id}", response_model=Cliente)
def obtener_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente_db = session.get(Cliente, cliente_id)
    if not cliente_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no existe")
    return cliente_db

# 4. Editar (Aquí está el cambio clave del video)
@rutas_clientes.patch("/clientes/{cliente_id}", response_model=Cliente)
def editar_cliente(cliente_id: int, cliente_datos: ClienteEditar, session: Session = Depends(get_session)):
    cliente_db = session.get(Cliente, cliente_id)
    if not cliente_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no existe")
    
    # El video usa model_dump y sqlmodel_update
    datos_dict = cliente_datos.model_dump(exclude_unset=True)
    cliente_db.sqlmodel_update(datos_dict) # <--- Este es el método correcto y limpio
    
    session.add(cliente_db)
    session.commit()
    session.refresh(cliente_db)
    return cliente_db

# 5. Eliminar
@rutas_clientes.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente_db = session.get(Cliente, cliente_id)
    if not cliente_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no existe")
    
    session.delete(cliente_db)
    session.commit()
    return {"mensaje": "Cliente eliminado exitosamente"}