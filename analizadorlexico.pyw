# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Nombre:       analizadorlexico.py
# Autor:        Cabral Torres Jorge(Topo)
# Creado:       13 abril del 2020
# Modificado:   
# Copyright:    (c) 2020 by Cabral Torres Jorge
# License:      Apache License 2.0
# ----------------------------------------------------------------------------

__version__ = "1.0"

# Versión Python: 3.5.2
# Versión PyQt5: 5.10.0
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *



class Nodo:
    def __init__(self, lexema=None, token=None, renglon=None):
        self.sig = None
        self.lexema = lexema
        self.token = token
        self.renglon = renglon



# ======================= CLASE Form ========================

class Form(QDialog):
    cabeza = Nodo()
    cabeza = None
    p = Nodo()
    estado = 0
    columna = 1
    valorMT = 1 
    numRenglon = 1
    caracter = 0
    lexema = ""
    errorEncontrado = False
    datos = []
    archivo = ""
    n = 0

    
    
    matriz = [
              #    L     D     +     -     *     =     .     ,     :     ;     <     >     (     )     "    Eb   tab    Nl   Eol   Eof    oc 
              #    0     1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19    20 
                [  1,    2,  103,  104,  105,  110,  112,  113,    7,  114,    6,    5,    8,  116,   11,    0,    0,    0,    0,    0,  503],#0
                [  1,    1,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100],#1
                [101,    2,  101,  101,  101,  101,    3,  101,  101,  101,  101,  101,  101,  101,  101,  101,  101,  101,  101,  101,  101],#2
                [500,    4,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500],#3
                [102,    4,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102],#4
                [107,  107,  107,  107,  107,  109,  107,  107,  107,  107,  107,  107,  107,  107,  107,  107,  107,  107,  107,  107,  107],#5
                [106,  106,  106,  106,  106,  108,  106,  106,  106,  106,  106,  111,  106,  106,  106,  106,  106,  106,  106,  106,  106],#6
                [119,  119,  119,  119,  119,  118,  119,  119,  119,  119,  119,  119,  119,  119,  119,  119,  119,  119,  119,  119,  119],#7
                [115,  115,  115,  115,    9,  115,  115,  115,  115,  115,  115,  115,  115,  115,  115,  115,  115,  115,  115,  115,  115],#8
                [  9,    9,    9,    9,   10,    9,    9,    9,    9,    9,    9,    9,    9,    9,    9,    9,    9,    9,    9,  501,    9],#9
                [  9,    9,    9,    9,    9,    9,    9,    9,    9,    9,    9,    9,    9,    0,    9,    9,    9,    9,    9,    9,    9],#10
                [ 11,   11,   11,   11,   11,   11,   11,   11,   11,   11,   11,   11,   11,   11,  117,   11,   11,   11,   502,  501,  11] #11    
    ]

    palReservadas = [
              #    0            1  
                [ "if",      "200"], #1 
                [ "then",    "201"], #2
                [ "else",    "202"], #3
                [ "while",   "203"], #4     
                [ "do",      "204"], #5
                [ "begin",   "205"], #6
                [ "end",     "206"], #7 
                [ "read",    "207"], #8 
                [ "write",   "208"], #9
                [ "var",     "209"], #10 
                [ "integer", "210"], #11 
                [ "program", "211"], #12 
                [ "true",    "212"], #13 
                [ "false",   "213"], #14 
                ["and",      "214"], #15 
                [ "or",      "215"], #17
                [ "not",     "216"], #18 
                [ "div",     "217"], #19 
                [ "real",    "218"], #20 
                [ "string",  "219"]  #21
    ]

    errores= [
              #         0                   1  
                [ "Se esperaba digito",   "500"], #0 
                [ "Eof inesperado",       "501"], #2
                [ "Eol inesperado",       "502"], #3    
                [ "Simbolo no valido",    "503"]  #4
    ]

    
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.setWindowTitle("Analizador lexico")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(400, 950)

        self.initUI()

    def initUI(self):
       
      # ================== WIDGET  QTableWidget ==================
      
        self.tabla = QTableWidget(self)

        # Deshabilitar edición
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Deshabilitar el comportamiento de arrastrar y soltar
        self.tabla.setDragDropOverwriteMode(False)

        # Seleccionar toda la fila
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Seleccionar una fila a la vez
        self.tabla.setSelectionMode(QAbstractItemView.SingleSelection)

        # Especifica dónde deben aparecer los puntos suspensivos "..." cuando se muestran
        # textos que no qt_
        self.tabla.setTextElideMode(Qt.ElideRight)# Qt.ElideNone

        # Establecer el ajuste de palabras del texto 
        self.tabla.setWordWrap(False)

        # Deshabilitar clasificación
        self.tabla.setSortingEnabled(False)

        # Establecer el número de columnas
        self.tabla.setColumnCount(3)

        # Establecer el número de filas
        self.tabla.setRowCount(0)

        # Alineación del texto del encabezado
        self.tabla.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)

        # Deshabilitar resaltado del texto del encabezado al seleccionar una fila
        self.tabla.horizontalHeader().setHighlightSections(False)

        # Hacer que la última sección visible del encabezado ocupa todo el espacio disponible
        self.tabla.horizontalHeader().setStretchLastSection(True)

        # Ocultar encabezado vertical
        self.tabla.verticalHeader().setVisible(False)

        # Dibujar el fondo usando colores alternados
        self.tabla.setAlternatingRowColors(True)

        # Establecer altura de las filas
        self.tabla.verticalHeader().setDefaultSectionSize(20)
        
        # self.tabla.verticalHeader().setHighlightSections(True)

        nombreColumnas = ("Lexema","Token","Renglon")

        # Establecer las etiquetas de encabezado horizontal usando etiquetas
        self.tabla.setHorizontalHeaderLabels(nombreColumnas)
        
        # Menú contextual
        self.tabla.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabla.customContextMenuRequested.connect(self.menuContextual)
        
        # Establecer ancho de las columnas
        for indice, ancho in enumerate((170, 100, 100), start=0):
            self.tabla.setColumnWidth(indice, ancho)

        self.tabla.resize(380, 850)
        self.tabla.move(10, 70)

      # =================== WIDGETS ==================
        
        self.labelDirecciondelArchivo = QLineEdit(self)
        self.labelDirecciondelArchivo.setPlaceholderText("Direccion del archivo(.txt)")
        self.labelDirecciondelArchivo.setGeometry(20,20,255,21)
        self.labelDirecciondelArchivo.move(10,8)
        
        botonBuscarArchivo = QPushButton("Buscar Archivo", self)
        botonBuscarArchivo.setFixedWidth(120)
        botonBuscarArchivo.move(270, 7)
        

        botonMostrarDatos = QPushButton("Mostrar datos", self)
        botonMostrarDatos.setFixedWidth(140)
        botonMostrarDatos.move(10, 37)

        menu = QMenu()
        for indice, columna in enumerate(nombreColumnas, start=0):
            accion = QAction(columna, menu)
            accion.setCheckable(True)
            accion.setChecked(True)
            accion.setData(indice)

            menu.addAction(accion)

        botonMostrarOcultar = QPushButton("Motrar/ocultar columnas", self)
        botonMostrarOcultar.setFixedWidth(180)
        botonMostrarOcultar.setMenu(menu)
        botonMostrarOcultar.move(210, 37)
        """
        botonEliminarFila = QPushButton("Eliminar fila", self)
        botonEliminarFila.setFixedWidth(100)
        botonEliminarFila.move(530, 20)
        """
        botonLimpiar = QPushButton("Limpiar", self)
        botonLimpiar.setFixedWidth(80)
        botonLimpiar.move(10, 925)

        botonCerrar = QPushButton("Cerrar", self)
        botonCerrar.setFixedWidth(80)
        botonCerrar.move(310, 925)

        
      # ======================== EVENTOS =========================

        botonBuscarArchivo.clicked.connect(self.pushButton_handler)
        botonMostrarDatos.clicked.connect(self.lexico)
        #botonEliminarFila.clicked.connect(self.eliminarFila)
        botonLimpiar.clicked.connect(self.limpiarTabla)
        botonCerrar.clicked.connect(self.close)

        menu.triggered.connect(self.mostrarOcultar)

  # ======================= FUNCIONES ============================
    def pushButton_handler(self):
        print("Botón presionado")
        self.open_dialog_box()
        
    def open_dialog_box(self):
        filtro = "Text File (*.txt)"
        filename = QFileDialog.getOpenFileName(self,"open a file" , "C://" , filtro)
        path = filename[0]
        print(path)
        self.archivo = path
        self.labelDirecciondelArchivo.setText(path)
       

    def lexico(self):
        try:
            self.cabeza = None
            self.caracter = 0
            self.numRenglon = 1
            file = open(self.archivo, "r", newline ='')
            while self.caracter != "":
                self.caracter = file.read(1)
                if self.caracter.isalpha():
                    self.columna = 0
                elif self.caracter.isdigit():
                    self.columna = 1
                else:
                    if self.caracter == "+":
                        self.columna = 2  
                    elif self.caracter == '-':
                        self.columna = 3   
                    elif self.caracter == '*':
                        self.columna = 4   
                    elif self.caracter == '=':
                        self.columna = 5  
                    elif self.caracter == '.':
                        self.columna = 6   
                    elif self.caracter == ',':
                        self.columna = 7 
                    elif self.caracter == ':':
                        self.columna = 8  
                    elif self.caracter == ';':
                        self.columna = 9      
                    elif self.caracter == '<':
                        self.columna = 10  
                    elif self.caracter == '>':
                        self.columna = 11   
                    elif self.caracter == '(':
                        self.columna = 12 
                    elif self.caracter == ')':
                        self.columna = 13    
                    elif self.caracter == '"':
                        self.columna = 14   
                    elif self.caracter == ' ': #Espacio en blanco
                        self.columna = 15   
                    elif self.caracter == chr(9): # Tabulacion 
                        self.columna = 16      
                    elif self.caracter == chr(10): # Nueva linea
                        self.numRenglon = self.numRenglon + 1   
                        self.columna = 17         
                    elif self.caracter == chr(13): #Eol Retorno de carro
                        self.columna = 18    
                    elif self.caracter == "": #Eof
                        self.columna = 19
                    else:
                        self.columna = 20
                
                self.valorMT = self.matriz[self.estado][self.columna]  

                if self.valorMT < 100:#cambiar de estado
                    self.estado = self.valorMT
                    if self.estado == 0:
                        self.lexema = ""
                    else:
                        self.lexema = self.lexema + self.caracter
                elif self.valorMT >= 100 and self.valorMT < 500:#estado final
                    if self.valorMT == 100:
                        self.validarSiEsPalabraReservada()

                    if (self.valorMT == 100 or self.valorMT == 101 or self.valorMT == 102 or self.valorMT == 106 or 
                        self.valorMT == 107 or self.valorMT == 115 or self.valorMT >= 200):
                        file.seek(file.tell()-1)
                    else:
                        self.lexema = self.lexema + self.caracter
                
                    self.insertarNodo()
                    self.estado = 0
                    self.lexema = ""
                else:
                    self.imprimirMensajeError()
                    break
            self.imprimirNodo()
            file.close()
        except Exception as e:
            print(e)


    def imprimirNodo(self):
        self.datos = []
        self.p = self.cabeza
        fila = 0
        
        while self.p != None:
            tupla = (self.p.lexema, str(self.p.token), str(self.p.renglon))
            self.datos.append(tupla)
            fila = fila + 1
            self.p = self.p.sig
        
        self.tabla.clearContents()

        row = 0
        for endian in self.datos:
            self.tabla.setRowCount(row + 1)
            
            idDato = QTableWidgetItem(endian[0])
            idDato.setTextAlignment(4)
            
            self.tabla.setItem(row, 0, QTableWidgetItem(endian[0]))
            self.tabla.setItem(row, 1, QTableWidgetItem(endian[1]))
            self.tabla.setItem(row, 2, QTableWidgetItem(endian[2]))
            row += 1
        

    def validarSiEsPalabraReservada(self):
        for self.palReservada in self.palReservadas:
            if self.lexema == self.palReservada[0]:
                self.valorMT = int(self.palReservada[1])

    def imprimirMensajeError(self):
        for self.error in self.errores:
            if str(self.valorMT) == self.error[1]:
                QMessageBox.critical(self,"Error","El error encontrado es: " + self.error[0])
            self.errorEncontrado = True

    
    def insertarNodo(self):
        nodo = Nodo(self.lexema,self.valorMT,self.numRenglon)
        if self.cabeza == None:
            self.cabeza = nodo
            self.p = self.cabeza
        else:
            self.p.sig = nodo
            self.p = nodo
            

    def mostrarOcultar(self, accion):
        columna = accion.data()
        
        if accion.isChecked():
            self.tabla.setColumnHidden(columna, False)
        else:
            self.tabla.setColumnHidden(columna, True)
    """
    def eliminarFila(self):
        filaSeleccionada = self.tabla.selectedItems()

        if filaSeleccionada:
            fila = filaSeleccionada[0].row()
            self.tabla.removeRow(fila)

            self.tabla.clearSelection()
        else:
            QMessageBox.critical(self, "Eliminar fila", "Seleccione una fila.   ",
                                 QMessageBox.Ok)
    """
    def limpiarTabla(self):
        self.tabla.clearContents()
        self.tabla.setRowCount(0)

    def menuContextual(self, posicion):
        indices = self.tabla.selectedIndexes()

        if indices:
            menu = QMenu()

            itemsGrupo = QActionGroup(self)
            itemsGrupo.setExclusive(True)
            
            menu.addAction(QAction("Copiar todo", itemsGrupo))

            columnas = [self.tabla.horizontalHeaderItem(columna).text()
                        for columna in range(self.tabla.columnCount())
                        if not self.tabla.isColumnHidden(columna)]

            copiarIndividual = menu.addMenu("Copiar individual") 
            for indice, item in enumerate(columnas, start=0):
                accion = QAction(item, itemsGrupo)
                accion.setData(indice)
                
                copiarIndividual.addAction(accion)

            itemsGrupo.triggered.connect(self.copiarTableWidgetItem)
            
            menu.exec_(self.tabla.viewport().mapToGlobal(posicion))

    def copiarTableWidgetItem(self, accion):
        filaSeleccionada = [dato.text() for dato in self.tabla.selectedItems()]
            
        if accion.text() == "Copiar todo":
            filaSeleccionada = tuple(filaSeleccionada)
        else:
            filaSeleccionada = filaSeleccionada[accion.data()]

        print(filaSeleccionada)

        return
    

    


                                
# ===============================================================           

if __name__ == "__main__":
    
    import sys
    
    aplicacion = QApplication(sys.argv)

    fuente = QFont()
    fuente.setPointSize(10)
    aplicacion.setFont(fuente)
    
    ventana = Form()
    ventana.show()

    sys.exit(aplicacion.exec_())
    
    