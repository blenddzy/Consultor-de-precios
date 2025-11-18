import pyodbc
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

class Database:
    def __init__(self):
        self.server = os.getenv('SQL_SERVER')
        self.database = os.getenv('SQL_DATABASE')
        self.driver = os.getenv('SQL_DRIVER')
        
    def get_connection(self):
        """Conecta a SQL Server"""
        try:
            connection_string = (
                f'DRIVER={self.driver};'
                f'SERVER={self.server};'
                f'DATABASE={self.database};'
                f'Trusted_Connection=yes;'
            )
            conn = pyodbc.connect(connection_string)
            return conn
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None
    
    def test_connection(self):
        """Prueba la conexión a la base de datos"""
        conn = self.get_connection()
        if conn:
            print("✅ Conexión exitosa a SQL Server")
            conn.close()
            return True
        else:
            print("❌ Error al conectar a SQL Server")
            return False
    
    def ejecutar_query(self, query, params=None):
        """Ejecuta una consulta SELECT"""
        try:
            conn = self.get_connection()
            if not conn:
                return None
            
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            resultados = cursor.fetchall()
            conn.close()
            return resultados
        except Exception as e:
            print(f"Error en query: {e}")
            return None
    
    def ejecutar_comando(self, comando, params=None):
        """Ejecuta un comando INSERT, UPDATE, DELETE"""
        try:
            conn = self.get_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            if params:
                cursor.execute(comando, params)
            else:
                cursor.execute(comando)
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error en comando: {e}")
            return False

# Crear instancia global
db = Database()
