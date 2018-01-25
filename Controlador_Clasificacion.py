# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QMessageBox,QTableWidgetItem
from PyQt5 import uic
from controlador_Index import Ventana_Principal
from PyQt5 import QtCore
import appmodel
class Ventana_Clasifica(QMainWindow):
 #Método constructor de la clase
 def __init__(self):
  #Iniciar el objeto QMainWindow
  QMainWindow.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
  self.genericas=[]
  self.violencia=[]
  self.table_model_violencia=0
  #self.ventana_Index=Ventana
  self.path_clasificar=""
  uic.loadUi("Ventana_Clasificacion.ui", self)
  self.setWindowTitle("Cambiando el título de la ventana")
 def con_tabla(self,violencia,genericas):
  self.violencia=violencia
  self.genericas=genericas
  #añadirle las cabeceras
  header = ["Titulo","Fecha","Descripcion"]
  #cargamos la tabla de violencia
  noticias=appmodel.CargarNoticias(self.violencia)
  data=appmodel.contenido_tabla(noticias)
  self.tbl_Vg.setColumnCount(3)
  self.tbl_Vg.setHorizontalHeaderLabels(header)
  self.tbl_Vg.setRowCount(len(data))
  r=0

  for i in data:
    c=0  
    for e in i:
        item=QTableWidgetItem(e)
        item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
        self.tbl_Vg.setItem(r,c, item)
        c=c+1
    r=r+1
#cargamos la tabla de genericas
  noticias=appmodel.CargarNoticias(self.genericas)
  data=appmodel.contenido_tabla(noticias)
  self.tbl_Nvg.setColumnCount(3)
  self.tbl_Nvg.setHorizontalHeaderLabels(header)
  self.tbl_Nvg.setRowCount(len(data))
  r=0

  for i in data:
    c=0  
    for e in i:
        item=QTableWidgetItem(e)
        item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
        self.tbl_Nvg.setItem(r,c,item )
        c=c+1
    r=r+1