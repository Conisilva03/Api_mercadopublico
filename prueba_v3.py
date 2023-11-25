import pyodbc
import requests
import time
import json
from datetime import datetime


#Funcion para convertir datetime
def parse_fecha(fecha_str):
    # Encontrar la posición del punto que separa los segundos de los microsegundos
    if fecha_str is not None:
        posicion_punto = fecha_str.find('.')
    else:
        posicion_punto=""
    # Eliminar los microsegundos y la 'Z' al final de la cadena
    if fecha_str is not None:
        fecha_sin_microsegundos = fecha_str[:posicion_punto] + 'Z'
    else:
        fecha_sin_microsegundos=""
    try:
        fecha = datetime.strptime(fecha_sin_microsegundos, "%Y-%m-%dT%H:%M:%SZ")
        return fecha
    except ValueError:
        #print("Formato de fecha incorrecto. Proporcione el formato correcto.")
        return None 



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
        print(f"Estado de respuesta: {response.status_code}")
        time.sleep(5)
        if response.status_code == 200:
            data = response.json()

            # Acceder a los datos de nivel superior del JSON
            
            fecha_creacion_str = data.get("FechaCreacion")
            # Encontrar la posición del punto que separa los segundos de los microsegundos
            posicion_punto = fecha_creacion_str.find('.')
            
            # Eliminar los microsegundos y la 'Z' al final de la cadena
            fecha_sin_microsegundos = fecha_creacion_str[:posicion_punto] + 'Z'

            fecha_creacion = datetime.strptime(fecha_sin_microsegundos, "%Y-%m-%dT%H:%M:%SZ")
   
            lista_ordenes = data.get("Listado", [])

            for orden in lista_ordenes:
                # Acceder a los detalles de cada orden
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

                # Acceder a las fechas anidadas de cada orden
                fechas = orden.get("Fechas", {})
                fechacreacion_str = fechas.get("FechaCreacion")
                # Encontrar la posición del punto que separa los segundos de los microsegundos
                posicionpunto = fechacreacion_str.find('.')

                # Eliminar los microsegundos y la 'Z' al final de la cadena
                fecha_sinmicrosegundos = fechacreacion_str[:posicionpunto] + 'Z'

                fechacreacion = datetime.strptime(fecha_sinmicrosegundos, "%Y-%m-%dT%H:%M:%SZ")

                fechaenvio = parse_fecha(fechas.get("FechaEnvio"))
                fechaaceptacion = parse_fecha(fechas.get("FechaAceptacion"))
                fechacancelacion = parse_fecha(fechas.get("FechaCancelacion"))
                fechaultimamodificacion = parse_fecha(fechas.get("FechaUltimaModificacion"))

                # Aceder a los Items
                tieneitems = orden.get("TieneItems")
                promediocalificacion = orden.get("PromedioCalificacion")
                cantidadevaluacion = orden.get("CantidadEvaluacion")
                descuentos = orden.get("Descuentos")
                cargos = orden.get("Cargos")
                totalneto = orden.get("TotalNeto")
                porcentajeiva = orden.get("PorcentajeIva")
                impuestos = orden.get("Impuestos")
                total = orden.get("Total")
                financiamiento = orden.get("Financiamiento")
                pais = orden.get("Pais")
                tipodespacho = orden.get("TipoDespacho")
                formapago = orden.get("FormaPago")

                # Acceder a los detalles del comprador
                comprador = orden.get("Comprador", {})
                codigoorganismo = comprador.get("CodigoOrganismo")
                nombreorganismo = comprador.get("NombreOrganismo")
                rutunidad = comprador.get("RutUnidad")
                codigounidad = comprador.get("CodigoUnidad")
                nombreunidad = comprador.get("NombreUnidad")
                actividad = comprador.get("Actividad")
                direccionunidad = comprador.get("DireccionUnidad")
                comunaunidad = comprador.get("ComunaUnidad")
                regionunidad = comprador.get("RegionUnidad")
                pais_u = comprador.get("Pais")
                nombrecontacto = comprador.get("NombreContacto")
                cargocontacto = comprador.get("CargoContacto")
                fonocontacto = comprador.get("FonoContacto")
                mailcontacto = comprador.get("MailContacto")
                
                # Acceder a los detalles del proveedor
                proveedor = orden.get("Proveedor", {})
                codigo02 = proveedor.get("Codigo")
                nombre02 = proveedor.get("Nombre")
                actividad02 = proveedor.get("Actividad")
                codigosucursal = proveedor.get("CodigoSucursal")
                nombresucursal = proveedor.get("NombreSucursal")
                rutsucursal = proveedor.get("RutSucursal")
                direccion = proveedor.get("Direccion")
                comuna = proveedor.get("Comuna")
                region = proveedor.get("Region")
                pais_s = proveedor.get("Pais")
                nombrecontacto = proveedor.get("NombreContacto")
                cargocontacto = proveedor.get("CargoContacto")
                fonocontacto = proveedor.get("FonoContacto")
                mailcontacto = proveedor.get("MailContacto")

                # Acceder a los detalles de Items
                items = orden.get("Items", {})
                
                cantidad02 = items.get("Cantidad")
                cantidad02 = int(cantidad02)
                
                listado = items.get("Listado", [])  # 'Listado' es una lista de items

            # Iterar a través de cada item en 'Listado'
            
            for items in listado:
                
                correlativo = items.get("Correlativo")
                codigocategoria = items.get("CodigoCategoria")
                categoria = items.get("Categoria")
                codigoproducto = items.get("CodigoProducto")
                especificacioncomprador = items.get("EspecificacionComprador")
                especificacionproveedor = items.get("EspecificacionProveedor")
                cantidad03 = int(items.get("Cantidad"))
                moneda = items.get("Moneda")
                precioneto = items.get("PrecioNeto")
                totalcargos = items.get("TotalCargos")
                totaldescuentos = items.get("TotalDescuentos")
                totalimpuestos = items.get("TotalImpuestos")
                total = items.get("Total")
                
                
                fecha_actualizacion = datetime.now().strftime("%Y-%m-%d")
                hora_actualizacion = datetime.now().strftime("%H:%M:%S")
                
                
                print("pre")
                sql = """INSERT INTO orden_compra
                (fechacreacion, codigo, nombre, codigoestado, codigolicitacion, descripcion, codigotipo, tipo, tipomoneda, codigoestadoproveedor, estadoproveedor, fechacreacionprov, fechaenvio, fechaaceptacion, fechacancelacion, fechaultimamodificacion, tieneitems, promediocalificacion, cantidadevaluacion, descuentos, cargos, totalneto, porcentajeiva, impuestos, total, financiamiento, pais, tipodespacho, formadepago, codigoorganismo, nombreorganismo, rutunidad, codigounidad, nombreunidad, actividad, direccionunidad, comunaunidad, regionunidad, pais_u, nombrecontacto, cargocontacto, fonocontacto, emailcontacto, codigoprov, nombreprov, actividadprov, codigosucursalprov, nombresucursalprov, rutsucursalprov, direccionsucursalprov, comunasucursalprov, regionsucursalprov, paissucursalprov, nombrecontactosucprov, cargocontactosucprov, telefonocontactosucprov, emailcontactosucprov, cantidaditems, correlativoitems, codigocategoriaitems, categoriaitem, codigoproducitem, especificcompitem, especificprovitem, cantidaditem, monedaitem, precionetoitem, totalcargositem, totaldescuentositem, totalimpuestositem, totalitem, condereg, fecha_actualizacion, hora_actualizacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?,?)"""
#                 print(type(fecha_creacion))
#                 print(fecha_creacion)
#                 print(type(codigo))
#                 print(codigo)
#                 print(type(nombre))
#                 print(nombre)
#                 print(type(codigoestado))
#                 print(codigoestado)
#                 print(type(codigolicitacion))
#                 print(codigolicitacion)
#                 print(type(descripcion))
#                 print(descripcion)
#                 print(type(codigotipo))
#                 print(codigotipo)
#                 print(type(tipo))
#                 print(tipo)
#                 print(type(tipomoneda))
#                 print(tipomoneda)
#                 print(type(codigoestadoproveedor))
#                 print(codigoestadoproveedor)
#                 print(type(estadoproveedor))
#                 print(estadoproveedor)
#                 print(type(fechacreacion))
#                 print(f"fechacreacion {fechacreacion}")
#                 print(type(fechaenvio))
#                 print(f"fechaenvio {fechaenvio}")
#                 print(type(fechaaceptacion))
#                 print(f"fechaaceptacion {fechaaceptacion}")
#                 print(type(fechacancelacion))
#                 print(f"fechacancelacion {fechacancelacion}")
#                 print(type(fechaultimamodificacion))
#                 print(f"fechaultimamodificacion {fechaultimamodificacion}")
#                 print(type(promediocalificacion))
#                 print((promediocalificacion))

                # print(type(cantidadevaluacion))
                # print((cantidadevaluacion))
                # print(type(descuentos))
                # print((descuentos))
                # print(type(cargos))
                # print((cargos))
                # print(type(totalneto))
                # print((totalneto))
                # print(type(porcentajeiva))
                # print((porcentajeiva))
                # print(type(impuestos))
                # print((impuestos))
                # print(type(total))
                # print((total))
                # print(type(financiamiento))
                # print((financiamiento))
                # print(type(pais))
                # print((pais))
                # print(type(tipodespacho))
                # print((tipodespacho))
                # print(type(formapago))
                # print((formapago))
                # print(type(codigoorganismo))
                # print((codigoorganismo))
                # print(type(nombreorganismo))
                # print((nombreorganismo))
                # print(type(rutunidad))
                # print((rutunidad))
                
                # print(type(codigounidad))
                # print((codigounidad))
                # print(type(nombreunidad))
                # print((nombreunidad))
                # print(type(actividad))
                # print((actividad))
                # print(type(direccionunidad))
                # print((direccionunidad))
                # print(type(comunaunidad))
                # print((comunaunidad))
                # print(type(regionunidad))
                # # print((regionunidad))
                # print(type(cantidad03))
                # print(type(int(cantidad03)))
                # print((cantidad03))
                # print(int(cantidad03))
                # # print(type(listado))
                # # print((listado))
                # # print("probando")
                # # print(type(codigoestado))
                # # print((codigoestado))
                # print("quiero saber el correlativo")
                # print(type(correlativo))
                # print((correlativo))
                # print(type(precioneto))
                # print((precioneto))
                
                
                


                
                try:
                    cursor.execute(sql, (fecha_creacion, codigo, nombre, codigoestado, codigolicitacion, descripcion, codigotipo, tipo, tipomoneda, codigoestadoproveedor, estadoproveedor, fechacreacion, fechaenvio, fechaaceptacion, fechacancelacion, fechaultimamodificacion, tieneitems, promediocalificacion, cantidadevaluacion, descuentos, cargos, totalneto, porcentajeiva, impuestos, total, financiamiento, pais, tipodespacho, formapago, codigoorganismo, nombreorganismo, rutunidad, codigounidad, nombreunidad, actividad, direccionunidad, comunaunidad, regionunidad, pais_u, nombrecontacto, cargocontacto, fonocontacto, mailcontacto, codigo02, nombre02, actividad02, codigosucursal, nombresucursal, rutsucursal, direccion, comuna, region, pais_s, nombrecontacto, cargocontacto, fonocontacto, mailcontacto, cantidad02, correlativo, codigocategoria, categoria, codigoproducto, especificacioncomprador, especificacionproveedor, cantidad03, moneda, precioneto, totalcargos, totaldescuentos, totalimpuestos, total, fecha_actualizacion, hora_actualizacion))

                    conn.commit()  

                    
                    print("Query executed successfully")

                except Exception as e:
                    # An exception occurred, indicating a failure
                    conn.rollback()  # Rollback changes if there's an error
                    print("Query execution failed:", str(e))
                print("post")
                
                print(f"FechaCreacion: {fecha_creacion}")
                
                print(f"Código: {codigo}")
                print(f"Nombre: {nombre}")
                print(f"CódigoEstado: {codigoestado}")
                print(f"Estado: {estado}")
                print(f"CodigoLicitacion: {codigolicitacion}")
                print(f"Descripcion: {descripcion}")
                print(f"CodigoTipo: {codigotipo}")
                print(f"Tipo: {tipo}")
                print(f"TipoMoneda: {tipomoneda}")

                # Acceder a prints de Proveedor
                print(f"CodigoEstadoProveedor: {codigoestadoproveedor}")
                print(f"EstadoProveedor: {estadoproveedor}")
                print(f"FechaCreacion: {fechacreacion}")
                print(f"FechaEnvio: {fechaenvio}")
                print(f"FechaAceptacion: {fechaaceptacion}")
                print(f"FechaCancelacion: {fechacancelacion}")
                print(f"FechaUltimaModificacion: {fechaultimamodificacion}")

                # Aceder a prints de Items
                print(f"PromedioCalificacion: {promediocalificacion}")
                print(f"CantidadEvaluacion: {cantidadevaluacion}")
                print(f"Descuentos: {descuentos}")
                print(f"Cargos: {cargos}")
                print(f"TotalNeto: {totalneto}")
                print(f"PorcentajeIva: {porcentajeiva}")
                print(f"Impuestos: {impuestos}")
                print(f"Total: {total}")
                print(f"Financiamiento: {financiamiento}")
                print(f"Pais: {pais}")
                print(f"TipoDespacho: {tipodespacho}")
                print(f"FormaPago: {formapago}")

                # Acceder a los detalles del comprador
                print(f"CodigoOrganismo: {codigoorganismo}")
                print(f"NombreOrganismo: {nombreorganismo}")
                print(f"RutUnidad: {rutunidad}")
                print(f"CodigoUnidad: {codigounidad}")
                print(f"NombreUnidad: {nombreunidad}")
                print(f"Actividad: {actividad}")
                print(f"DireccionUnidad: {direccionunidad}")
                print(f"ComunaUnidad: {comunaunidad}")
                print(f"RegionUnidad: {regionunidad}")
                print(f"Pais: {pais_u}")
                print(f"NombreContacto: {nombrecontacto}")
                print(f"CargoContacto: {cargocontacto}")
                print(f"FonoContacto: {fonocontacto}")
                print(f"MailContacto: {mailcontacto}")
                
            
                # Acceder a los detalles del proveedor
                print(f"Codigo: {codigo02}")
                print(f"Nombre: {nombre02}")
                print(f"Actividad: {actividad02}")
                print(f"CodigoSucursal: {codigosucursal}")
                print(f"NombreSucursal: {nombresucursal}")
                print(f"RutSucursal: {rutsucursal}")
                print(f"Direccion: {direccion}")
                print(f"Comuna: {comuna}")
                print(f"Region: {region}")
                print(f"Pais: {pais}")
                print(f"NombreContacto: {nombrecontacto}")
                print(f"CargoContacto: {cargocontacto}")
                print(f"FonoContacto: {fonocontacto}")
                print(f"MailContacto: {mailcontacto}")


                # Acceder a los detalles de item en 'Listado'

                print(f"Cantidad: {cantidad02}")
                print(f"Correlativo: {correlativo}")
                print(f"CodigoCategoria: {codigocategoria}")
                print(f"Categoria: {categoria}")
                print(f"CodigoProducto: {codigoproducto}")
                print(f"EspecificacionComprador: {especificacioncomprador}")
                print(f"EspecificacionProveedor: {especificacionproveedor}")
                print(f"Cantidad: {cantidad03}")
                print(f"Moneda: {moneda}")
                print(f"PrecioNeto: {precioneto}")
                print(f"TotalCargos: {totalcargos}")
                print(f"TotalDescuentos: {totaldescuentos}")
                print(f"TotalImpuestos: {totalimpuestos}")
                print(f"Total: {total}")



except Exception as e:
    print(f"Se produjo un error: {e}")

# Cerrar la conexión
cursor.close()
conn.close()
