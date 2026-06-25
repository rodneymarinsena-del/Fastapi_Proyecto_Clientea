from fastapi import FastAPI
from app.enrutadores import clientes, facturas, transacciones

app = FastAPI()

# Registro de enrutadores 
app.include_router(clientes.rutas_clientes, tags=["clientes"])
app.include_router(facturas.rutas_facturas, tags=["facturas"])
app.include_router(transacciones.rutas_transacciones, tags=["transacciones"])