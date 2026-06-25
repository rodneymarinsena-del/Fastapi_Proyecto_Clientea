from pydantic import BaseModel
from .clientes import Cliente

class FacturaBase(BaseModel):
    cliente: Cliente
    monto: float
    descripcion: str

class Factura(FacturaBase):
    id: int | None = None

class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(FacturaBase):
    pass