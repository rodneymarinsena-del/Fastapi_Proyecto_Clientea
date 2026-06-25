from pydantic import BaseModel

class TransaccionBase(BaseModel):
    factura_id: int
    tipo: str  # Ejemplo: 'pago' o 'reembolso'
    monto: float

class Transaccion(TransaccionBase):
    id: int | None = None

class TransaccionCrear(TransaccionBase):
    pass