from sqlmodel import SQLModel, create_engine, Session

# 1. Definir el nombre del archivo de la base de datos
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# 2. Crear el motor de la base de datos (conectar)
# connect_args es necesario para SQLite en multihilo
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# 3. Crear las tablas (esta función se llamará al iniciar la app)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 4. Función para inyectar la sesión en los endpoints
def get_session():
    with Session(engine) as session:
        yield session