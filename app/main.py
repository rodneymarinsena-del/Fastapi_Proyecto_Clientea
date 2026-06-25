from fastapi import FastAPI
from app.enrutadores import clientes, facturas, transacciones
from app.database import create_db_and_tables  

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(clientes.rutas_clientes, tags=["clientes"])
app.include_router(facturas.rutas_facturas, tags=["facturas"])
app.include_router(transacciones.rutas_transacciones, tags=["transacciones"])