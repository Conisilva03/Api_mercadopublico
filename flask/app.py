from flask import jsonify, render_template, redirect ,url_for
from flask import Flask, request
import pyodbc
import webbrowser
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        fecha = request.form['fecha']
        # Convertir la fecha a formato Year-Month-Day
        date_components = fecha.split('-')
        year, month, day = date_components
        
        # Datos de conexión a la base de datos
        #server = 'DESKTOP-N26HD66'
        server = 'EstebanBLL\SQLEXPRESS'
        database = 'mercadop'
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

        try:
            # Crear la conexión a la base de datos
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()

            # Consulta SQL
            cursor.execute(f"SELECT CODIGO, NOMBRE, fechacreacion FROM orden_compra WHERE YEAR(fechacreacion)={year} AND MONTH(fechacreacion)={month} AND DAY(fechacreacion)={day}")

            # Obtener los resultados de la consulta
            rows = cursor.fetchall()
            api_response = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

            # Cerrar la conexión
            cursor.close()
            conn.close()

            # Redirigir a la página de resultados con los datos obtenidos
            return render_template('resultados.html', api_response=api_response)

        except Exception as e:
            error_message = f"Se produjo un error: {e}"
            return render_template('error.html', error_message=error_message)

    return render_template('menu.html')

# Nueva ruta para manejar la solicitud de rescatar_ordenes
@app.route('/rescatar_ordenes', methods=['GET'])
def rescatar_ordenes():
    import subprocess
    subprocess.run(["python", "conexion_sql.py"])

    return jsonify({"message": "Se cargaron las ordenes de compra en la Base de datos."})

# Nueva ruta para manejar la solicitud de obtener_ordenes_fecha
@app.route('/obtener_ordenes_fecha', methods=['GET'])
def obtener_ordenes_fecha():
    try:
        subprocess.run(["python", "orden_compra_fecha.py"])
    
        #return render_template('orden_compra_fecha.html', api_response=example_api_response)
        #return redirect(url_for('orden_compra_fecha'))
        
        return jsonify({"message": "Se cargaron las órdenes de compra en la Base de datos."})
    
    except Exception as e:
        # Mensaje de error en caso de excepción durante la ejecución del script
        print(f"Error en obtener_ordenes_fecha: {str(e)}")
        return render_template('error.html', error_message=f"Error: {str(e)}. No se cargaron las ordenes de compra por fecha correctamente."), 500

# Nueva ruta para manejar la plantilla orden_compra_fecha.html
@app.route('/orden_compra_fecha', methods=['GET'])
def orden_compra_fecha():
    # Puedes agregar lógica adicional aquí si es necesario
    return render_template('orden_compra_fecha.html')

if __name__ == '__main__':
    url = 'http://127.0.0.1:5000'
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'  # Ruta ejecutable de Chrome
    webbrowser.get(chrome_path).open(url)  # Abre en Chrome
    app.run(port=5000)