from flask import Flask, render_template, request
import pyodbc
import webbrowser

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    api_response = None
    if request.method == 'POST':
        
        fecha = request.form['fecha']

        # Convertir la fecha a formato Year-Month-Day
        date_components = fecha.split('-')
        year = date_components[0]
        month = date_components[1]
        day = date_components[2]
        
        # Datos de conexión a la base de datos
        server = 'DESKTOP-N26HD66'
        database = 'mercadop'
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

        try:
            # Crear la conexión a la base de datos
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()

            # Consulta SQL
            cursor.execute(f"SELECT CODIGO, NOMBRE, fechacreacion FROM orden_compra where YEAR(fechacreacion)={year} and MONTH(fechacreacion)={month} and DAY(fechacreacion)={day}");

            # Obtener los resultados de la consulta
            rows = cursor.fetchall()
            api_response = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

            for row in rows:
                print(row)  # Puedes imprimir o procesar los resultados como desees

        except Exception as e:
            print(f"Se produjo un error: {e}")

        finally:
            # Cerrar la conexión
            cursor.close()
            conn.close()
    
    return render_template('index.html', api_response=api_response)

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')  # Abre el navegador al iniciar la aplicación
    app.run(port=5000)  # Ejecuta la aplicación Flask en el puerto 5000

