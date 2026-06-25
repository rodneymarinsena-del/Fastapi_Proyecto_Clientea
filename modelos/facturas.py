from pydantic import BaseModel

class FacturaBase(BaseModel):
    cliente_id: int
    monto: float
    descripcion: str

class Factura(FacturaBase):
    id: int | None = None

class FacturaCrear(FacturaBase):
    pass