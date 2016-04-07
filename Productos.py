# -*- coding: utf-8 -*-


import sqlite3 as produtos
from gi.repository import Gtk
from InformeReportLab import ReportLab
settings = Gtk.Settings.get_default()
settings.props.gtk_button_images = True
class Products:
    """Este apartado realiza las declaraciones iniciales de las variables ventana e inicializa los builder"""
    #Creamos acceso a las ventanas de glade
    archivoVentanaPrincipal = "VentanaPrincipal1.glade"
    archivoVentanaConsulta = "VentanaConsulta.glade"
    archivoVentanaIntroducir = "VentanaIntroducir.glade"
    archivoVentanaEliminar = "VentanaEliminar.glade"
    archivoVentanaAlerta = "Alertacodigo.glade"
    archivoVentanaArticuloEliminado = "VentanaArticuloEliminado.glade"
    #Creamos constructores de GTK para las interfaces
    builderVentanaAlerta = Gtk.Builder()
    builderVentanaPrincipal = Gtk.Builder()
    builderVentanaConsulta = Gtk.Builder()
    builderVentanaIntroducir = Gtk.Builder()
    builderVentanaEliminar = Gtk.Builder()
    builderVentanaArticuloEliminado = Gtk.Builder()
    #Añadimos los archivos a los constructores de la interface
    builderVentanaPrincipal.add_from_file(archivoVentanaPrincipal)
    builderVentanaConsulta.add_from_file(archivoVentanaConsulta)
    builderVentanaIntroducir.add_from_file(archivoVentanaIntroducir)
    builderVentanaEliminar.add_from_file(archivoVentanaEliminar)
    builderVentanaAlerta.add_from_file(archivoVentanaAlerta)
    builderVentanaArticuloEliminado.add_from_file(archivoVentanaArticuloEliminado)

    #Recogemos las ventanas contenedoras
    ventanaEntrada = builderVentanaPrincipal.get_object("VentanaPrincipal")
    ventanaConsultas = builderVentanaConsulta.get_object("VentanaConsulta")
    ventanaIntroducir = builderVentanaIntroducir.get_object("VentanaIntroducir")
    ventanaEliminar = builderVentanaEliminar.get_object("VentanaEliminar")
    ventanaAlertaCodigo = builderVentanaAlerta.get_object("AlertaCodigo")
    ventanaAlertaArchivoEliminado = builderVentanaArticuloEliminado.get_object("VentanaArticuloEliminado")
    ventanaEntrada.show_all()
    #Conectamenos a la base de datos y creamos un cursor para recorrerla
    bd = produtos.connect("productos.dat")
    print(bd)
    cursor = bd.cursor()



#Funciones de búsqueda y modificación:
    def al_buscar(self, busqueda):
        """Este método realizara las busquedas"""
        self.consolaVenta.set_text("")
        self.cajaNombreConsultada.set_text("")
        self.cajaPrecioConsultada.set_text("")
        self.cajaCantidadConsultada.set_text("")
        self.cajaEstadoConsultada.set_text("")
        self.cajaSpecsConsultada.set_text("")
        self.cajaMarcaConsultada.set_text("")

        if self.RadioCod.get_active():
            #Recogemos el codigo de la caja de texto
            codigo = self.cajaIdConsulta.get_text().upper()
            #Buscamos el codigo recogido en la base de datos
            self.cursor.execute("Select * from productos where Codigo='"+codigo+"'")
            #Recorremos el cursor y mostraremos por pantalla si existe
            for producto in self.cursor:
                self.cajaNombreConsultada.set_text(str(producto[1]))
                self.cajaPrecioConsultada.set_text(str(producto[2]))
                self.cajaCantidadConsultada.set_text(str(producto[3]))
                self.cajaEstadoConsultada.set_text(str(producto[4]))
                self.cajaSpecsConsultada.set_text(str(producto[5]))
                self.cajaMarcaConsultada.set_text(str(producto[6]))

        elif self.RadioNomb.get_active():
             #Recogemos el codigo de la caja de texto
            nombre = self.cajaIdConsulta.get_text()
            #Buscamos el codigo recogido en la base de datos
            self.cursor.execute("Select * from productos where Nombre='"+nombre+"'")
            #Recorremos el cursor y mostraremos por pantalla si existe
            for producto in self.cursor:
                self.cajaNombreConsultada.set_text(str(producto[1]))
                self.cajaPrecioConsultada.set_text(str(producto[2]))
                self.cajaCantidadConsultada.set_text(str(producto[3]))
                self.cajaEstadoConsultada.set_text(str(producto[4]))
                self.cajaSpecsConsultada.set_text(str(producto[5]))
                self.cajaMarcaConsultada.set_text(str(producto[6]))




    def introducirStock(self, introducir):
        """Este metodo introduce o stock"""
        id = self.cajaIntroducirCodId.get_text().upper()
        nombre = self.cajaIntroducirNombre.get_text().upper()
        precio = self.cajaIntroducirPrecio.get_text().upper()
        cantidad = self.cajaIntroducirCantidad.get_text().upper()
        estado = self.comboEstado.get_active_text()
        specs = self.cajaIntroducirSpecs.get_text().upper()
        marca = self.cajaIntroducirMarca.get_text().upper()

        self.limpiarIntroducir(self)
        print("inserte")
        self.cursor.execute("select codigo from productos")
        #Recogemos los codigos de los productos para despues descartar si esta o no en la base
        codigos = self.cursor.fetchall()
        existe=False
        for producto in codigos:

            idCompare = str(producto)
            #Si esta en la base; existe pasa a True y no se añadirá a la base
            if idCompare[2:4]==id:
                print("Ya existe ese codigo!!")
                existe = True
                self.ventanaAlertaCodigo.show_all()

        if existe==False:
            #Introducimos valores en la tabla
            self.cursor.execute("insert into productos values('" + id + "','" + nombre + "','" + precio + "','" + cantidad + "','" + estado + "','" + specs + "','" + marca + "')")
            print("Insertado")
            #Importante efectuar commits en cada modificacion para asegurarnos la integridad de los datos en la misma
            self.bd.commit()

        existe=False


    def al_modificar(self, modificacion):
        """Este metodo fai as modificacions na base de datos"""
        #Definimos variables de texto que recogeran el texto que hay en las cajas
        nombre = self.cajaNombreConsultada.get_text().upper()
        precio = self.cajaPrecioConsultada.get_text().upper()
        cantidad = self.cajaCantidadConsultada.get_text().upper()
        specs = self.cajaSpecsConsultada.get_text().upper()
        marca = self.cajaMarcaConsultada.get_text().upper()
        id = self.cajaIdConsulta.get_text().upper()
        estado = self.cajaEstadoConsultada.get_text().upper()
        #Actualizamos los datos de la tabla en esa posicion mediante un Update
        self.cursor.execute(
            "update productos set Nombre ='" + nombre + "',Precio='" + precio + "',Cantidad='" + cantidad + "',Estado='" + estado + "',Specs='" + specs +"',Marca='" + marca + "'" + " where Codigo='" + id + "'")
        print("Modificado")
        self.consolaVenta.set_text("Artículo modíficado")
        #Importante efectuar commits en cada modificacion para asegurarnos la integridad de los datos en la misma
        self.bd.commit()
        #Borramos las cajas usadas ya actualizadas
        self.cajaNombreConsultada.set_text("")
        self.cajaPrecioConsultada.set_text("")
        self.cajaCantidadConsultada.set_text("")
        self.cajaEstadoConsultada.set_text("")
        self.cajaMarcaConsultada.set_text("")
        self.cajaSpecsConsultada.set_text("")


    def Eliminar(self, eliminado):
        """Esta funcion elimina los articulos solicitados de la base de datos"""
        #Recoje el codigo al igual que la función buscar; la diferencia es que esta ejecute un delete pasando como parámetro el código
        cajaEliminar = self.cajaEliminar.get_text()
        self.cursor.execute("delete from productos where Codigo ='" + cajaEliminar + "'")
        print("Borrado")
        self.ventanaAlertaArchivoEliminado.show_all()
        #Importante efectuar commits en cada modificacion para asegurarnos la integridad de los datos en la misma
        self.bd.commit()
        #Borramos la caja de Eliminar ya usada
        self.cajaEliminar.set_text("")



#Funciones de limpieza de cajas de texto según Ventana
    def click_limpiarConsulta(self,limpieza):
        """Este metodo limpia cajas de texto"""
        self.cajaIdConsulta.set_text("")
        self.cajaNombreConsultada.set_text("")
        self.cajaPrecioConsultada.set_text("")
        self.cajaCantidadConsultada.set_text("")
        self.cajaSpecsConsultada.set_text("")
        self.cajaMarcaConsultada.set_text("")
        self.cajaEstadoConsultada.set_text("")
        self.cajaNventas.set_text("")



    def limpiarIntroducir(self, introduccion):
        """Este metodo limpia cajas de texto"""
        self.cajaIntroducirCodId.set_text("")
        self.cajaIntroducirNombre.set_text("")
        self.cajaIntroducirPrecio.set_text("")
        self.cajaIntroducirCantidad.set_text("")
        self.cajaIntroducirMarca.set_text("")
        self.cajaIntroducirSpecs.set_text("")


    def realizar_venta(self, venta):
        """Este metodo hace ventas y reduce stock"""
        id = self.cajaIdConsulta.get_text().upper()
        cantidadInicial = self.cajaCantidadConsultada.get_text()
        cantidadVenta = self.cajaNventas.get_text()
        cantidadF = float(cantidadInicial) - float(cantidadVenta)
        cantidadI = int(cantidadF)
        cantidad = str(cantidadI)


        if cantidadI==0:
            self.cursor.execute("delete from productos where Codigo ='" + id + "'")
            self.consolaVenta.set_text("            YA NO QUEDAN ARTICULOS!           ")
        elif cantidadI<=-1:
            self.consolaVenta.set_text("         NO HAY ARTICULOS SUFICIENTES!        ")
        else:
            self.cursor.execute("update productos set Cantidad='"+cantidad+"' where Codigo='"+id+"'")
            print("Modificado")
            self.cajaCantidadConsultada.set_text(str(int(cantidad)))
            self.consolaVenta.set_text("             ARTICULO/S VENDIDO!!              ")

        self.bd.commit()


    def generar_informe(self, entrada):
        """Este metodo genera el informe de la base de datos"""
        ReportLab()




#Funciones de muestra y ocultacion de ventanas según clicks:
    def click_introducir(self, entrada):
        """Definimos click Introducir"""
        self.ventanaEntrada.hide()
        self.ventanaIntroducir.show_all()


    def click_consultar(self, consulta):
        """Definimos click Consultar"""
        self.ventanaEntrada.hide()
        self.consolaVenta.set_text("")
        self.ventanaConsultas.show_all()


    def Eliminar_articulo(self,eliminado):
        """Definimos click eliminar"""
        self.ventanaEntrada.hide()
        self.ventanaEliminar.show_all()



#Funciones de vuelta a la ventana principal
    def click_volverConsulta(self, vuelta):
        """Definimos click volver"""
        self.click_limpiarConsulta(self)
        self.ventanaConsultas.hide()
        self.ventanaEntrada.show_all()


    def volverIntroducir(self, vuelta):
        """Definimos click volver"""
        self.limpiarIntroducir(self)
        self.ventanaIntroducir.hide()
        self.ventanaEntrada.show_all()


    def volverEliminar(self, vuelta):
        """Definimos click volver"""
        self.cajaEliminar.set_text("")
        self.ventanaEliminar.hide()
        self.ventanaEntrada.show_all()



#Declaración Inicial de handlers(manejadores, señales) y entrada de ventana Principal al iniciar la aplicación
    def __init__(self):
        """Definimos los botones, cajas y demas widgets"""
        #Mostramos la ventana principal

        self.ventanaEntrada.show_all();


        #Manejadores; funciones definidas en Glade con su equivalencia en Python
        manejadores = {
                  "click_limpiarConsulta":self.click_limpiarConsulta,
                  "click_volverConsulta":self.click_volverConsulta,
                  "limpiarCamposIntroducir":self.limpiarIntroducir,
                  "click_introducirStock":self.introducirStock,
                  "Eliminar_articulo":self.Eliminar_articulo,
                  "click_introducir": self.click_introducir,
                  "volverIntroducir":self.volverIntroducir,
                  "click_consultar": self.click_consultar,
                  "volverEliminar":self.volverEliminar,
                  "click_modificar":self.al_modificar,
                  "click_vender":self.realizar_venta,
                  "cerrarAlertaCodigo":self.alerta,
                  "informe":self.generar_informe,
                  "al_buscar":self.al_buscar,
                  "Terminar1":self.Terminar,
                  "Terminar2":self.Terminar,
                  "Terminar3":self.Terminar,
                  "Terminar":self.Terminar,
                  "Eliminar":self.Eliminar,
                  "botonOk":self.BotonOk
        }
        #Conectamos los constructores con los manejadores
        self.builderVentanaPrincipal.connect_signals(manejadores)
        self.builderVentanaConsulta.connect_signals(manejadores)
        self.builderVentanaIntroducir.connect_signals(manejadores)
        self.builderVentanaEliminar.connect_signals(manejadores)
        self.builderVentanaAlerta.connect_signals(manejadores)
        self.builderVentanaArticuloEliminado.connect_signals(manejadores)

        #Recojemos las cajas de las ventanas
        self.cajaIdConsulta = self.builderVentanaConsulta.get_object("cajaIdConsulta")
        self.cajaNventas = self.builderVentanaConsulta.get_object("cajaVenta")
        self.cajaNombreConsultada = self.builderVentanaConsulta.get_object("cajaNombreConsultada")
        self.consolaVenta = self.builderVentanaConsulta.get_object("LConsola")
        self.cajaPrecioConsultada = self.builderVentanaConsulta.get_object("cajaPrecioConsultada")
        self.cajaEstadoConsultada = self.builderVentanaConsulta.get_object("cajaEstadoConsultado")
        self.cajaMarcaConsultada = self.builderVentanaConsulta.get_object("cajaMarcaConsultada")
        self.cajaSpecsConsultada = self.builderVentanaConsulta.get_object("cajaSpecsConsultada")
        self.cajaCantidadConsultada = self.builderVentanaConsulta.get_object("cajaCantidadConsultada")
        self.cajaIntroducirCodId = self.builderVentanaIntroducir.get_object("cajaIntroducirCodId")
        self.cajaIntroducirMarca = self.builderVentanaIntroducir.get_object("cajaIntroducirMarca")
        self.cajaIntroducirSpecs = self.builderVentanaIntroducir.get_object("cajaIntroducirSpecs")
        self.cajaIntroducirNombre = self.builderVentanaIntroducir.get_object("cajaIntroducirNombre")
        self.cajaIntroducirPrecio = self.builderVentanaIntroducir.get_object("cajaIntroducirPrecio")
        self.comboEstado = self.builderVentanaIntroducir.get_object("comboStock")
        self.cajaIntroducirCantidad = self.builderVentanaIntroducir.get_object("cajaIntroducirCantidad")
        self.cajaEliminar = self.builderVentanaEliminar.get_object("cajaEliminar")
        self.RadioCod = self.builderVentanaConsulta.get_object("radioCodigo")
        self.RadioNomb = self.builderVentanaConsulta.get_object("radioNombre")




    def alerta(self, alerta):
        """Definimos Ventana Alerta"""
        self.ventanaAlertaCodigo.hide()



    def BotonOk(self,ok):
        """Definimos click OK"""
        self.ventanaAlertaArchivoEliminado.hide()



#Función de cierre del programa
    def Terminar(self, dos, tres):
        """Definimos cel cierre del programa"""
        #Cerramos todas las ventanas y el main
        self.ventanaEntrada.connect("delete-event", Gtk.main_quit)
        self.ventanaIntroducir.connect("delete-event", Gtk.main_quit)
        self.ventanaEliminar.connect("delete-event", Gtk.main_quit)
        self.ventanaConsultas.connect("delete-event", Gtk.main_quit)
        Gtk.main_quit()


Products()
Gtk.main()
#Queda pendiente la inclusión de pequeñas consolas  que avisen del resultado de los eventos
#(si se ha actualizado,borrado,... con exito o no) y la discriminacion de datos
#segun sean caracteres o números