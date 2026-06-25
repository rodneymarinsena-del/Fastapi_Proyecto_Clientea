from pydantic import BaseModel

class TransaccionBase(BaseModel):
    factura_id: int
    tipo: str  
    monto: float

class Transaccion(TransaccionBase):
    id: int | None = None

class TransaccionCrear(TransaccionBase):
    pass

class TransaccionEditar(TransaccionBase):
    pass