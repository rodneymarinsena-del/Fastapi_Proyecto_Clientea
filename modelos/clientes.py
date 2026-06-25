from pydantic import BaseModel

class ClienteBase(BaseModel):
    nombre: str
    email: str
    descripcion: str

class Cliente(ClienteBase):
    id: int | None = None

class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass