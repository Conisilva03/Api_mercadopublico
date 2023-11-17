import pyodbc
import requests

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
        
        if response.status_code == 200:
            data = response.json()

            # Acceder a los datos de nivel superior del JSON
            cantidad = data.get("Cantidad")
            fecha_creacion = data.get("FechaCreacion")
            version = data.get("Version")

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
                fechacreacion = fechas.get("FechaCreacion")
                fechaenvio = fechas.get("FechaEnvio")
                fechaaceptacion = fechas.get("FechaAceptacion")
                fechacancelacion = fechas.get("FechaCancelacion")
                fechaultimamodificacion = fechas.get("FechaUltimaModificacion")

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

                 # Acceder a los detalles de Items
                items = orden.get("Items", {})
                listado = items.get("Listado", [])  # 'Listado' es una lista de items

            # Iterar a través de cada item en 'Listado'
            
            for items in listado:
                cantidad = items.get("Cantidad")
                correlativo = items.get("Correlativo")
                codigocategoria = items.get("CodigoCategoria")
                categoria = items.get("Categoria")
                codigoproducto = items.get("CodigoProducto")
                especificacioncomprador = items.get("EspecificacionComprador")
                especificacionproveedor = items.get("EspecificacionProveedor")
                cantidad = items.get("Cantidad")
                moneda = items.get("Moneda")
                precioneto = items.get("PrecioNeto")
                totalcargos = items.get("TotalCargos")
                totaldescuentos = items.get("TotalDescuentos")
                totalimpuestos = items.get("TotalImpuestos")
                total = items.get("Total")


                print(f"Cantidad: {cantidad}")
                print(f"FechaCreacion: {fecha_creacion}")
                print(f"Version: {version}")

               
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

                # Acceder a los detalles de item en 'Listado'

                print(f"Cantidad: {cantidad}")
                print(f"Correlativo: {correlativo}")
                print(f"CodigoCategoria: {codigocategoria}")
                print(f"Categoria: {categoria}")
                print(f"CodigoProducto: {codigoproducto}")
                print(f"EspecificacionComprador: {especificacioncomprador}")
                print(f"EspecificacionProveedor: {especificacionproveedor}")
                print(f"Cantidad: {cantidad}")
                print(f"Moneda: {moneda}")
                print(f"PrecioNeto: {precioneto}")
                print(f"TotalCargos: {totalcargos}")
                print("TotalDescuentos: {totaldescuentos}")
                print(f"TotalImpuestos: {totalimpuestos}")
                print(f"Total: {total}")



except Exception as e:
    print(f"Se produjo un error: {e}")

# Cerrar la conexión
cursor.close()
conn.close()
