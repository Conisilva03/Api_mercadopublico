import requests
import time
from datetime import datetime

# Definimos una constante para el ticket de API.
API_TICKET = "F8537A18-6766-4DEF-9E59-426B4FEE2844"
BASE_URL = "https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json"

def llamada_api_segura(url, params, max_reintentos=3):
    """
    Realiza una llamada segura a la API con reintentos y retroceso exponencial.

    :param url: La URL del endpoint de la API.
    :param params: Los parámetros para la solicitud.
    :param max_reintentos: Número máximo de reintentos antes de rendirse.
    :return: La respuesta JSON de la API.
    """
    retroceso = 1  # Comenzamos con un retraso de 1 segundo
    for i in range(max_reintentos):
        try:
            respuesta = requests.get(url, params=params)
            respuesta.raise_for_status()  # Provoca una excepción si la solicitud HTTP retornó un código de estado de error
            return respuesta.json()
        except requests.HTTPError as e:
            if e.response.status_code == 10500 and i < max_reintentos - 1:
                print(f"Se han detectado peticiones simultáneas. Reintentando en {retroceso} segundos...")
                time.sleep(retroceso)
                retroceso *= 2  # Retroceso exponencial
            else:
                # Vuelve a lanzar la excepción si se supera el número máximo de reintentos o para otros códigos de error
                raise
        except requests.RequestException as e:
            print(f"Error en la conexión con la API: {e}")
            if i < max_reintentos - 1:
                print(f"Reintentando en {retroceso} segundos...")
                time.sleep(retroceso)
                retroceso *= 2
            else:
                raise

def obtener_orden_compra_por_codigo(codigo):
    params = {'codigo': codigo, 'ticket': API_TICKET}
    return llamada_api_segura(BASE_URL, params)

def obtener_ordenes_por_estado_fecha(estado, fecha=None):
    if fecha is None:
        fecha = datetime.now().strftime('%d%m%Y')
    params = {'fecha': fecha, 'estado': estado, 'ticket': API_TICKET}
    return llamada_api_segura(BASE_URL, params)

def obtener_ordenes_por_codigo_organismo(fecha, codigo_organismo):
    params = {'fecha': fecha, 'CodigoOrganismo': codigo_organismo, 'ticket': API_TICKET}
    return llamada_api_segura(BASE_URL, params)

def obtener_ordenes_por_codigo_proveedor(fecha, codigo_proveedor):
    params = {'fecha': fecha, 'CodigoProveedor': codigo_proveedor, 'ticket': API_TICKET}
    return llamada_api_segura(BASE_URL, params)


def preguntar_y_ejecutar_accion():
    while True:
        print("\n¿Qué acción te gustaría realizar?")
        print("1. Obtener una orden de compra por código.")
        print("2. Obtener órdenes de compra por estado y fecha.")
        print("3. Obtener órdenes de compra por código de organismo público y fecha.")
        print("4. Obtener órdenes de compra por código de proveedor y fecha.")
        print("5. Salir.")
        opcion = input("Selecciona una opción (1-5): ")
        
        if opcion == '1':
            codigo = input("Ingresa el código de la orden de compra: ")
            try:
                resultado = obtener_orden_compra_por_codigo(codigo)
                print(resultado)
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == '2':
            estado = input("Ingresa el estado de la orden de compra: ")
            fecha = input("Ingresa la fecha (DDMMYYYY) o deja en blanco para la fecha actual: ")
            try:
                resultado = obtener_ordenes_por_estado_fecha(estado, fecha if fecha else None)
                print(resultado)
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == '3':
            codigo_organismo = input("Ingresa el código del organismo público: ")
            fecha = input("Ingresa la fecha (DDMMYYYY): ")
            try:
                resultado = obtener_ordenes_por_codigo_organismo(fecha, codigo_organismo)
                print(resultado)
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == '4':
            codigo_proveedor = input("Ingresa el código del proveedor: ")
            fecha = input("Ingresa la fecha (DDMMYYYY): ")
            try:
                resultado = obtener_ordenes_por_codigo_proveedor(fecha, codigo_proveedor)
                print(resultado)
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == '5':
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Inténtalo de nuevo.")

def main():
    try:
        preguntar_y_ejecutar_accion()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")

if __name__ == '__main__':
    main()
