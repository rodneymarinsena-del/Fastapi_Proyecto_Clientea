from pydantic import BaseModel, computed_field
from typing import List
from datetime import datetime
from .clientes import Cliente
from .transacciones import Transaccion

class FacturaBase(BaseModel):
    # El cliente se asignará dinámicamente en el main
    cliente: Cliente | None = None
    fecha: datetime = datetime.now()
    transacciones: List[Transaccion] = []

    @computed_field
    @property
    def valor_total(self) -> float:
        return 0.0  # Lógica de cálculo pendiente para el futuro

class Factura(FacturaBase):
    id: int | None = None

class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(FacturaBase):
    pass