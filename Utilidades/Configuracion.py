import os
from dotenv import load_dotenv
import pyodbc

# Cargar variables del entorno desde .env
load_dotenv()

class Configuracion:
    @staticmethod
    def obtener_conexion():
        strConnection = (
            f"Driver={{{os.environ.get('DB_DRIVER')}}};"
            f"Server={os.environ.get('DB_SERVER')};"
            f"Database={os.environ.get('DB_DATABASE')};"
            f"PORT={os.environ.get('DB_PORT')};"
            f"UID={os.environ.get('DB_USER')};"
            f"PWD={os.environ.get('DB_PASSWORD')};"
        )
        return pyodbc.connect(strConnection)
