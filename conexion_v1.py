import requests
import pyodbc
from datetime import datetime
from flask import Flask, render_template, request
import webbrowser

app = Flask(__name__)

server = 'DESKTOP-N26HD66'
database = 'mercadop'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
api_key = "673FD54D-B2AB-4A6F-861E-DE76A79FF9EA"
url = f"https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json?fecha=15112023&CodigoOrganismo=111875&ticket=F8537A18-6766-4DEF-9E59-426B4FEE2844"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    lista_ordenes = data.get("Listado", [])
    print(f"Se encontraron {len(lista_ordenes)} órdenes de compra.")

    try:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()

        @app.route('/', methods=['GET', 'POST'])
        def formulario():
            mensaje = None

            if request.method == 'POST':
                try:
                    dia = request.form['dia']
                    mes = request.form['mes']
                    anio = request.form['anio']

                    cursor.execute("TRUNCATE TABLE apioc01")
                    print("Tabla vaciada.")

                    for orden in lista_ordenes:
                        codigo = orden.get("Codigo")
                        nombre = orden.get("Nombre")
                        codigo_estado = orden.get("CodigoEstado")
                        print(f"Procesando orden: {codigo}")
                        print(f"Nombre: {nombre}")
                        print(f"CodigoEstado: {codigo_estado}")

                        fecha_actualizacion = datetime.now().strftime("%Y-%m-%d")
                        hora_actualizacion = datetime.now().strftime("%H:%M:%S")

                        if codigo and nombre and codigo_estado is not None:
                            sql = """INSERT INTO apioc01 
                                    (codigo, nombre, codigoestado, condreg, fecha_actualizacion, hora_actualizacion) 
                                    VALUES (?, ?, ?, 0, ?, ?)"""
                            cursor.execute(sql, codigo, nombre, codigo_estado, fecha_actualizacion, hora_actualizacion)
                            #print(f"Orden {codigo} insertada.")

                    conn.commit()
                    print("Cambios guardados en la base de datos.")

                except Exception as e:
                    print(f"Se produjo un error: {e}")

            return render_template('Consulta_fechas_oc.html')

    except Exception as e:
        print(f"Se produjo un error: {e}")

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')  # Abre el navegador al iniciar la aplicación
    app.run(port=5000)  # Ejecuta la aplicación Flask en el puerto 5000
