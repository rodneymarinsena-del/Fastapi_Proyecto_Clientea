

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

# Importamos las dependencias necesarias de la base de datos y modelos
from app.database import get_session
from app.modelos.clientes import Cliente, ClienteCrear, ClienteEditar

# Definimos el router para los clientes
rutas_clientes = APIRouter()


# 1. Endpoint para Crear un Cliente (POST)
@rutas_clientes.post("/clientes/", response_model=Cliente)
def crear_cliente(cliente_datos: ClienteCrear, session: Session = Depends(get_session)):
    # Validamos y creamos el objeto cliente
    cliente_db = Cliente.model_validate(cliente_datos)
    session.add(cliente_db)
    session.commit()
    session.refresh(cliente_db)
    return cliente_db


# 2. Endpoint para Listar todos los Clientes (GET)
@rutas_clientes.get("/clientes/", response_model=List[Cliente])
def listar_clientes(session: Session = Depends(get_session)):
    # Ejecutamos la consulta para obtener todos los registros
    clientes = session.exec(select(Cliente)).all()
    return clientes


# 3. Endpoint para obtener un solo Cliente (GET)
@rutas_clientes.get("/clientes/{cliente_id}", response_model=Cliente)
def obtener_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente_db = session.get(Cliente, cliente_id)
    
    # Validamos si existe antes de retornar
    if not cliente_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cliente no existe"
        )
    return cliente_db


# 4. Endpoint para Editar un Cliente (PATCH)
@rutas_clientes.patch("/clientes/{cliente_id}", response_model=Cliente)
def editar_cliente(cliente_id: int, cliente_datos: ClienteEditar, session: Session = Depends(get_session)):
    # Primero buscamos el cliente en la base de datos
    cliente_db = session.get(Cliente, cliente_id)
    if not cliente_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cliente no existe"
        )
    
    # Convertimos a diccionario y usamos sqlmodel_update para cambios parciales
    datos_dict = cliente_datos.model_dump(exclude_unset=True)
    cliente_db.sqlmodel_update(datos_dict)
    
    # Guardamos los cambios
    session.add(cliente_db)
    session.commit()
    session.refresh(cliente_db)
    return cliente_db


# 5. Endpoint para Eliminar un Cliente (DELETE)
@rutas_clientes.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int, session: Session = Depends(get_session)):
    # Buscamos el cliente antes de intentar borrar
    cliente_db = session.get(Cliente, cliente_id)
    if not cliente_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cliente no existe"
        )
    
    # Eliminamos el objeto de la sesión
    session.delete(cliente_db)
    session.commit()
    return {"mensaje": "Cliente eliminado exitosamente"}