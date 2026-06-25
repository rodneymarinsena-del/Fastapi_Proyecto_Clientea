from pydantic import BaseModel, computed_field
from typing import List
from datetime import datetime
from .clientes import Cliente
from .transacciones import Transaccion

class FacturaBase(BaseModel):
    cliente: Cliente | None = None
    fecha: datetime = datetime.now()
    transacciones: List[Transaccion] = []

    @computed_field
    @property
    def valor_total(self) -> float:
        total_factura = 0.0
        for transaccion in self.transacciones:
            total_factura += (transaccion.cantidad * transaccion.valor_unitario)
        return total_factura

class Factura(FacturaBase):
    id: int | None = None

class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(FacturaBase):
    pass