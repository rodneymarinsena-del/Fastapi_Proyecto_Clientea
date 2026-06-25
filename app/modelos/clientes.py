from sqlmodel import SQLModel, Field
from typing import Optional

# 1. Clase base para validación (no es tabla)
class ClienteBase(SQLModel): # Cambiamos de BaseModel a SQLModel
    nombre: str
    email: str
    descripcion: str

# 2. Clase para la base de datos (con table=True)
class Cliente(ClienteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# 3. Esquemas para los endpoints (estos NO llevan table=True)
class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(SQLModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    descripcion: Optional[str] = None