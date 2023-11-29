from flask import Flask, render_template, redirect, url_for, request
import pyodbc
import webbrowser
import subprocess

app = Flask(__name__)

# Función para establecer conexión a la base de datos y realizar la consulta
def consultar_ordenes_por_fecha(year, month, day):
    # Establecer la conexión con la base de datos
    server = 'DESKTOP-N26HD66'
    database = 'mercadop'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Consulta SQL para obtener órdenes de compra por fecha
    query = f"SELECT CODIGO, NOMBRE, fechacreacion FROM orden_compra WHERE YEAR(fechacreacion)={year} AND MONTH(fechacreacion)={month} AND DAY(fechacreacion)={day}"
    cursor.execute(query)

    # Obtener los resultados de la consulta
    rows = cursor.fetchall()

    # Cerrar la conexión con la base de datos
    cursor.close()
    conn.close()

    return rows

@app.route('/')
def redireccionar():
    return redirect(url_for('menu'))

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/index', methods=['GET', 'POST'])
def mostrar_index():
    if request.method == 'POST':
        fecha = request.form['fecha']
        date_components = fecha.split('-')
        year, month, day = date_components

        # Llama a la función para consultar órdenes por fecha
        api_response = consultar_ordenes_por_fecha(year, month, day)
        return render_template('resultados.html', api_response=api_response)
    
    return render_template('index.html')

@app.route('/rescatar_ordenes')
def rescatar_ordenes():
    return render_template('rescatar.html')

@app.route('/ejecutar_rescate_ordenes', methods=['POST'])
def ejecutar_rescate_ordenes():
    # Lógica para rescatar órdenes de compra desde la API y guardar en la base de datos
    # ...

    return "Se han consultado tantas órdenes y se han insertado tantas órdenes."  # Mensaje de respuesta

@app.route('/ejecutar_prueba_v3', methods=['POST'])
def ejecutar_prueba_v3():
    try:
        # Ejecutar el archivo prueba_v3.py usando subprocess
        subprocess.run(["python", "prueba_v3.py"])
        print("El archivo prueba_v3.py se ha ejecutado exitosamente.")
    except Exception as e:
        print(f"Error al ejecutar prueba_v3.py: {e}")

    return redirect(url_for('menu'))

if __name__ == '__main__':
    url = 'http://127.0.0.1:5000'
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'  # Ruta ejecutable de Chrome
    webbrowser.get(chrome_path).open(url)  # Abre en Chrome
    app.run(port=5000)
