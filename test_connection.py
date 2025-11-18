from database import db

print("Probando conexión a SQL Server...")
print(f"Servidor: {db.server}")
print(f"Base de datos: {db.database}")
print()

if db.test_connection():
    print("✅ ¡La aplicación puede conectarse a tu SQL Server!")
else:
    print("❌ No se pudo conectar. Verifica los datos en .env")
