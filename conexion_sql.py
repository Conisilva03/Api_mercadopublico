import requests
import pyodbc
from datetime import datetime

server = 'DESKTOP-N26HD66'
database = 'mercadop'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
api_key = "673FD54D-B2AB-4A6F-861E-DE76A79FF9EA"
url = f"https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json?ticket=673FD54D-B2AB-4A6F-861E-DE76A79FF9EA"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    lista_ordenes = data.get("Listado", [])
    print(f"Se encontraron {len(lista_ordenes)} órdenes de compra, vamos a filtrar")

    try:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()

            # Paso 2: Vaciar la tabla antes de comenzar a insertar nuevos datos
            cursor.execute("TRUNCATE TABLE apioc01")
            print("Tabla vaciada.")

            # Paso 3: Procesar las respuestas de la API
            for orden in lista_ordenes:
                codigo = orden.get("Codigo")
                nombre = orden.get("Nombre")
                codigo_estado = orden.get("CodigoEstado")
                codigo02 = str(codigo)[:4]
                #print(f"codigo02: {codigo02}")

                if codigo02 == "3178":
                    print(f"Procesando orden: {codigo}")
                    print(f"Nombre: {nombre}")
                    print(f"CodigoEstado: {codigo_estado}")

                    fecha_actualizacion = datetime.now().strftime("%Y-%m-%d")
                    hora_actualizacion = datetime.now().strftime("%H:%M:%S")

                    # Paso 4: Insertar los nuevos registros en la tabla
                    if codigo and nombre and codigo_estado is not None:
                        sql = """INSERT INTO apioc01 
                                    (codigo, nombre, codigoestado, condreg, fecha_actualizacion, hora_actualizacion) 
                                    VALUES (?, ?, ?, 0, ?, ?)"""
                        cursor.execute(sql, (codigo, nombre, codigo_estado, fecha_actualizacion, hora_actualizacion))
                        print(f"Orden {codigo} insertada.")

                    else:
                        print({codigo})

            conn.commit()
            print("Cambios guardados en la base de datos.")

    except Exception as e:
        print(f"Se produjo un error: {e}")

else:
    print(f"Error al realizar la solicitud al API: {response.status_code}")
