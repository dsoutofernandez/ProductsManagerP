
import os

from reportlab.platypus import Paragraph
from reportlab.platypus import Image
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

import sqlite3 as dbapi
class ReportLab:

    bd = dbapi.connect("productos.dat")
    cursor = bd.cursor()

    cursor.execute("select * from productos")
    tablaBaseDatos = []

    cabecera = ["CODIGO","ARTICULO","PRECIO","UNIDADES","ESTADO","DESCRIPCION","MARCA"]
    cabecera2 = ["","","","","","",""]


    tablaBaseDatos.append(cabecera)
    tablaBaseDatos.append(cabecera2)

    for fila in cursor:
        tablaBaseDatos.append(fila)

    taboa = Table(tablaBaseDatos)

    guion = []
    guion.append(taboa)

    document = SimpleDocTemplate("Informe.pdf", pagesize=A4, showBoundary=0)
    document.build(guion)
    cursor.close()
    bd.close()

