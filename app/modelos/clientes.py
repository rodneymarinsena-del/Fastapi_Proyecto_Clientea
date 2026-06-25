from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

# Importación para el tipado que no causa ciclos
if TYPE_CHECKING:
    from app.modelos.facturas import Factura

# 1. Clase base para validación
class ClienteBase(SQLModel):
    nombre: str
    email: str
    descripcion: str

# 2. Clase para la base de datos (con table=True)
class Cliente(ClienteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # ESTA LÍNEA ES LA QUE FALTA PARA QUE EL ORM FUNCIONE
    facturas: List["Factura"] = Relationship(back_populates="cliente")

# 3. Esquemas para los endpoints
class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(SQLModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    descripcion: Optional[str] = None