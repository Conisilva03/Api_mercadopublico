import pyodbc
import requests
import time

# Datos de conexión a la base de datos
server = 'DESKTOP-N26HD66'
database = 'mercadop'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# Crear la conexión a la base de datos
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

try:
    # Consulta SQL
    cursor.execute("SELECT CODIGO, NOMBRE, CODIGOESTADO, CONDREG, FECHA_ACTUALIZACION, HORA_ACTUALIZACION FROM apioc01;")
     
    # Obtener todos los registros
    ocoms = cursor.fetchall()
    
    for ocom in ocoms:
        codigo = ocom[0]
        nombre = ocom[1]
        codigoestado = ocom[2]

        # Realizar acciones con los datos obtenidos
        url = f"https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json?codigo={codigo}&ticket=673FD54D-B2AB-4A6F-861E-DE76A79FF9EA"
        response = requests.get(url)
        print(response.status_code)
        time.sleep(5)
        if response.status_code == 200:
            data = response.json()

            lista_ordenes = data.get("Listado", [])
            
            for orden in lista_ordenes:
                # Acceder a los detalles del comprador
                comprador = orden.get("Comprador", {})
                codigo = orden.get("Codigo")
                nombre = orden.get("Nombre")
                codigoestado = orden.get("CodigoEstado")
                estado = orden.get("Estado")
                codigolicitacion = orden.get("CodigoLicitacion")
                descripcion = orden.get("Descripcion")
                codigotipo = orden.get("CodigoTipo")
                tipo = orden.get("Tipo")
                tipomoneda = orden.get("TipoMoneda")
                codigoestadoproveedor = orden.get("CodigoEstadoProveedor")
                estadoproveedor = orden.get("EstadoProveedor")

                # Acceder a las fechas anidadas
                fechas = orden.get("Fechas", {})
                fechacreacion = fechas.get("FechaCreacion")
                fechaenvio = fechas.get("FechaEnvio")
                fechaaceptacion = fechas.get("FechaAceptacion")
                fechacancelacion = fechas.get("FechaCancelacion")
                fechaultimamodificacion = fechas.get("FechaUltimaModificacion")

                print(f"Código: {codigo}")
                print(f"Nombre: {nombre}")
                print(f"CódigoEstado: {codigoestado}")
                print(f"Estado: {estado}")
                print(f"CodigoLicitacion: {codigolicitacion}")
                print(f"Descripcion: {descripcion}")
                print(f"CodigoTipo: {codigotipo}")
                print(f"Tipo: {tipo}")
                print(f"TipoMoneda: {tipomoneda}")
                print(f"CodigoEstadoProveedor: {codigoestadoproveedor}")
                print(f"EstadoProveedor: {estadoproveedor}")
                print(f"FechaCreacion: {fechacreacion}")
                print(f"FechaEnvio: {fechaenvio}")
                print(f"FechaAceptacion: {fechaaceptacion}")
                print(f"FechaCancelacion: {fechacancelacion}")
                print(f"FechaUltimaModificacion: {fechaultimamodificacion}")
        
except Exception as e:
    print(f"Se produjo un error: {e}")
   
# Cerrar la conexión
cursor.close()
conn.close()
