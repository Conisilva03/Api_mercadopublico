import requests
from datetime import datetime
import json

# Definimos las constantes para el acceso a la API.
API_TICKET = "F8537A18-6766-4DEF-9E59-426B4FEE2844"  # Reemplazar con tu ticket real
BASE_URL = "https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json"

def obtener_ordenes_por_estado_fecha(estado, fecha):
    """
    Obtiene órdenes de compra por estado y fecha.
    """
    params = {
        'fecha': fecha,
        'estado': estado,
        'ticket': API_TICKET
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()   # Esto lanzará una excepción si la API retorna un error
    return response.json()

def guardar_json(datos, nombre_archivo):
    """
    Guarda los datos en formato JSON en un archivo.
    """
    with open(nombre_archivo, 'w') as archivo:  
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

# Definir el estado y la fecha que deseas consultar
estado = "enviadaproveedor"  # Ejemplo de estado
fecha = datetime.now().strftime('%d%m%Y')  # Fecha actual en formato DDMMYYYY

# Llamamos a la función para obtener las órdenes de compra
try:
    datos_ordenes = obtener_ordenes_por_estado_fecha(estado, fecha)
    # Guardamos los datos en un archivo JSON
    guardar_json(datos_ordenes, 'ordenes_compra_estado_fecha.json')
    print("Archivo guardado con éxito.")
except requests.HTTPError as e:
    print(f"Error en la respuesta de la API: {e.response.status_code}")
except Exception as e:
    print(f"Ha ocurrido un error: {e}")

