from pydantic import BaseModel
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str
    email: str
    descripcion: str

class Cliente(ClienteBase):
    id: int

class ClienteCrear(ClienteBase):
    pass