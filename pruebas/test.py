import requests
import json

# URL del API de Mercado Público
api_key = "F8537A18-6766-4DEF-9E59-426B4FEE2844"
v_estado = "aceptada"

url = f"https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json?estado={v_estado}&ticket={api_key}"

try:
    # Realizar la solicitud a la API
    response = requests.get(url)

    # Comprueba si la respuesta fue exitosa
    response.raise_for_status()

    # Acceder al contenido JSON
    data = response.json()
    print("Datos recibidos del API.")

    # Nombre del archivo donde se guardará el JSON
    filename = 'ordenes_compra.json'

    # Escribir el JSON en el archivo
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Los datos han sido guardados en {filename}")

except requests.HTTPError as http_err:
    print(f"Error al realizar la solicitud HTTP: {http_err}")
except Exception as err:
    print(f"Ocurrió un error: {err}")
