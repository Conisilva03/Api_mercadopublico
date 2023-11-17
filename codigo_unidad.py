import pyodbc
import requests

# Datos de conexión a la base de datos
server = 'DESKTOP-N26HD66'
database = 'mercadop'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# Crear la conexión a la base de datos
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Consulta SQL
cursor.execute("SELECT CODIGO, NOMBRE, CODIGOESTADO, CONDREG, FECHA_ACTUALIZACION, HORA_ACTUALIZACION FROM apioc01;")

ocom = cursor.fetchone()
while ocom:
    codigo=(ocom[0])
    nombre=(ocom[1])
    
    #print(codigo)
    #print(nombre)
    
    ocom = cursor.fetchone()
    
    url = f"https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json?codigo={codigo}&ticket=673FD54D-B2AB-4A6F-861E-DE76A79FF9EA"


    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        lista_ordenes = data.get("Listado", [])
        print(f"Se encontraron {len(lista_ordenes)} órdenes de compra en mercado publico.")
        
        for orden in lista_ordenes:
            codigo01 = orden.get("Codigo")
            nombre01 = orden.get("Nombre")
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
            codigo = proveedor.get("Codigo")
            nombre = proveedor.get("Nombre")
            actividad = proveedor.get("Actividad")
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

             # Filtrar por CodigoUnidad "4099"
            if codigounidad == '4099':
                # Procesa e imprime la orden si CodigoUnidad es igual a "4099"
                # Imprimir los detalles de la orden
                print(f"Código: {codigo01}")
                print(f"Nombre: {nombre01}") 
                print(f"CodigoEstado: {codigoestado}")
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
                print(f"Codigo: {codigo}")
                print(f"Nombre: {nombre}")
                print(f"Actividad: {actividad}")
                print(f"CodigoSucursal: {codigosucursal}")
                print(f"NombreSucursal: {nombresucursal}")
                print(f"RutSucursal: {rutsucursal}")
                print(f"Direccion: {direccion}")
                print(f"Comuna: {comuna}")
                print(f"Region: {region}")
                print(f"Pais: {pais_s}")
                print(f"NombreContacto: {nombrecontacto}")
                print(f"CargoContacto: {cargocontacto}")
                print(f"FonoContacto: {fonocontacto}")
                print(f"MailContacto: {mailcontacto}")
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
                

            


            

        

    

       

            
            # Imprimir los datos
          # print(f"Procesando codigo: {codigo01}")
           # print(f"Procesando nombre: {nombre01}")
           # print(f"Procesando codigoestado: {codigoestado}")
           # print(f"Procesando estado: {estado}")
            #print(f"Procesando codigolicitacion: {codigolicitacion}")
           # print(f"Procesando descripcion: {descripcion}")
           # print(f"Procesando codigotipo: {codigotipo}")
           # print(f"Procesando tipo: {tipo}")
           # print(f"Procesando tipomoneda: {tipomoneda}")
           # print(f"Procesando codigoestadoproveedor: {codigoestadoproveedor}")
           # print(f"Procesando estadoproveedor: {estadoproveedor}")
            
           # print(f"Procesando fechacreacion: {fechacreacion}")
           # print(f"Procesando fechaenvio: {fechaenvio}")
           # print(f"Procesando fechaaceptacion: {fechaaceptacion}")
           # print(f"Procesando fechacancelacion: {fechacancelacion}")
        # ''' print(f"Procesando fechaultimamodificacion: {fechaultimamodificacion}")
            
        # print(f"Procesando tieneitems: {tieneitems}")
        # print(f"Procesando promediocalificacion: {promediocalificacion}")
        # print(f"Procesando cantidadevaluacion: {cantidadevaluacion}")
        # print(f"Procesando descuentos: {descuentos}")
        # print(f"Procesando cargos: {cargos}")
        # print(f"Procesando totalneto: {totalneto}")
        # print(f"Procesando porcentajeiva: {porcentajeiva}")
        # print(f"Procesando impuestos: {impuestos}")
        # print(f"Procesando total: {total}")
        # print(f"Procesando financiamiento: {financiamiento}")
        # print(f"Procesando pais: {pais}")
        # print(f"Procesando tipodespacho: {tipodespacho}")
        # print(f"Procesando formapago: {formapago}")
            
        #         # Imprimir los datos del comprador
        #     print(f"Procesando codigoorganismo: {codigoorganismo}")
        #     print(f"Procesando nombreorganismo: {nombreorganismo}")
        #     print(f"Procesando rutunidad: {rutunidad}") 
        #     print(f"Procesando codigounidad: {codigounidad}")
        #     print(f"Procesando nombreunidad: {nombreunidad}")       
        #     print(f"Procesando actividad: {actividad}")     
        #     print(f"Procesando direccionunidad: {direccionunidad}")     
        #     print(f"Procesando comunaunidad: {comunaunidad}")     
        #     print(f"Procesando regionunidad: {regionunidad}")     
        #     print(f"Procesando pais_u: {pais_u}")     
        #     print(f"Procesando nombrecontacto: {nombrecontacto}")     
        #     print(f"Procesando cargocontacto: {cargocontacto}")     
        #     print(f"Procesando fonocontacto: {fonocontacto}")     
        #     print(f"Procesando mailcontacto: {mailcontacto}")   
            
            
        #         # Imprimir los datos del proveedor
        #     print(f"Procesando codigo: {codigo}")
        #     print(f"Procesando nombre: {nombre}")
        #     print(f"Procesando actividad: {actividad}")
        #     print(f"Procesando codigosucursal: {codigosucursal}")
        #     print(f"Procesando nombresucursal: {nombresucursal}")
        #     print(f"Procesando rutsucursal: {rutsucursal}")
        #     print(f"Procesando direccion: {direccion}")
        #     print(f"Procesando comuna: {comuna}")
        #     print(f"Procesando region: {region}")
        #     print(f"Procesando pais: {pais}")
        #     print(f"Procesando nombrecontacto: {nombrecontacto}")
        #     print(f"Procesando cargocontacto: {cargocontacto}")
        #     print(f"Procesando fonocontacto: {fonocontacto}")
        #     print(f"Procesando mailcontacto: {mailcontacto}")
         
                    
        #         # Imprimir los datos del item individual
        #     print(f"Procesando cantidad: {cantidad}")
        #     print(f"Procesando correlativo: {correlativo}")
        #     print(f"Procesando codigocategoria: {codigocategoria}")
        #     print(f"Procesando categoria: {categoria}")
        #     print(f"Procesando codigoproducto: {codigoproducto}")
        #     print(f"Procesando especificacioncomprador: {especificacioncomprador}")
        #     print(f"Procesando especificacionproveedor: {especificacionproveedor}")
        #     print(f"Procesando cantidad: {cantidad}")
        #     print(f"Procesando moneda: {moneda}")
        #     print(f"Procesando precioneto: {precioneto}")
        #     print(f"Procesando totalcargos: {totalcargos}")
        #     print(f"Procesando totaldescuentos: {totaldescuentos}")
        #     print(f"Procesando totalimpuestos: {totalimpuestos}")
        #     print(f"Procesando total: {total}") 
            
            else:
                # Solo muestra el mensaje de que no corresponde a '4099 Hospital Naval Almirante Adriazola'
                print(f"El código de unidad {codigounidad} no corresponde a '4099 Hospital Naval Almirante Adriazola'")
                continue  # Salta al siguiente elemento en lista_ordenes        
                    
            
            
            
# Cerrar la conexión
cursor.close()
conn.close()




