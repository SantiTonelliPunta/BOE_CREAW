import asyncio
import asyncpg
from config.settings import settings

async def init_database():
    try:
        # Conectar a PostgreSQL
        conn = await asyncpg.connect(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database='postgres',  # Conectamos a la base por defecto
            host=settings.POSTGRES_HOST
        )
        
        # Crear base de datos si no existe
        await conn.execute('''
            SELECT 'CREATE DATABASE boe_db'
            WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'boe_db')
        ''')
        
        await conn.close()
        
        # Reconectar a la nueva base de datos
        conn = await asyncpg.connect(settings.POSTGRES_URL)
        
        # Leer y ejecutar el script SQL
        with open('database/init.sql', 'r') as file:
            sql = file.read()
            await conn.execute(sql)
        
        print("Base de datos inicializada correctamente")
        
    except Exception as e:
        print(f"Error inicializando la base de datos: {e}")
    finally:
        if conn:
            await conn.close()

if __name__ == "__main__":
    asyncio.run(init_database()) 