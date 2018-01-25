# -*- coding: utf-8 -*-
import sys
import appmodel
import cargardata
import os
import pickle
import model
import Noticia
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QMessageBox,QTableWidgetItem,QWidget,QHeaderView
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtCore import QSize
from PyQt5 import uic
from PyQt5 import QtCore
def pallet(x,y):
    oImage = QImage('.'+os.path.sep+'utiliti'+os.path.sep+"copy.jpg")
    sImage = oImage.scaled(QSize(x,y))                   # resize Image to widgets size
    palette = QPalette()
    palette.setBrush(10, QBrush(sImage))                     # 10 = Windowrole
    return palette
#from Controlador_Clasificacion import Ventana_Clasifica
#Clase heredada de QMainWindow (Constructor de ventanas)
class Ventana_Principal(QMainWindow):
 #Método constructor de la clase
 def __init__(self):
  #Iniciar el objeto QMainWindow
  QMainWindow.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
  
  self.path_clasificar=""
  self.path_entrenar=""
  uic.loadUi("Ventana_Index.ui", self)
  self.setWindowTitle("Clasificador de noticias")
  self.setPalette(pallet(892,675))
  #añadimos los modelos
  nam_model=appmodel.obtener_modelos('.'+os.path.sep+'modelos')
  self.cbx_Modelos.addItems(nam_model)
  self.btt_Desc.clicked.connect(self.selec_carpeta_Desc)
  self.btt_Clasificar_2.clicked.connect(self.clasificar)
  self.btt_Entreno.clicked.connect(self.selec_carpeta_Entre)
  self.btt_Crear_Model.clicked.connect(self.Crear_Modelo)
 def Crear_Modelo(self):
      path='.'+os.path.sep+'modelos'+os.path.sep+self.txt_Nombre.text()+'.txt'
      dst='.'+os.path.sep+'Entrenamiento'+os.path.sep+self.txt_Nombre.text()
      
      categorias=cargardata.obtener_path_noticias_entrenamiento(self.path_entrenar)
      if(self.txt_Nombre.text()!=""):
          if not os.path.exists(path):
             
              if(self.path_entrenar!=""):
                  data,target_names,target=cargardata.load_files(self.path_entrenar)
                  if(len(data)>0):
                        modelo = model.crearModelo(data,target,target_names, outpath=path) 
                        if(modelo):
                            os.makedirs(dst)
                            pa=self.path_entrenar+os.path.sep+categorias[0]
                            shutil.move(pa,dst)
                            pa=self.path_entrenar+os.path.sep+categorias[1]
                            shutil.move(self.path_entrenar+os.path.sep+categorias[1],dst)
                            QMessageBox.about(self, "CREACION", "Modelo Creado")
                            self.cbx_Modelos.addItem(self.txt_Nombre.text())
                        else:
                            QMessageBox.about(self, "ERROR", "ERROR AL CREAR EL MODELO")
                  else : 
                      QMessageBox.about(self, "ERROR", "Datos mal cargado")
          else:
              QMessageBox.about(self, "ERROR", "El nombre introducido ya existe")
      else: 
          QMessageBox.about(self, "ERROR", "Introduce un nombre") 
 def selec_carpeta_Entre(self):
    file = str(QFileDialog.getExistingDirectory(self, "Select Directory")) 
    if file:
        self.path_entrenar=file
 def selec_carpeta_Desc(self):
    file = str(QFileDialog.getExistingDirectory(self, "Select Directory")) 
    if file:
        self.path_clasificar=file
        
 def clasificar(self):
        if(self.path_clasificar!=""):
            nombre_modelo=self.cbx_Modelos.currentText()
            path_modelo='.'+os.path.sep+'modelos'+os.path.sep+nombre_modelo+".txt"
            dirnoticias=self.path_clasificar
            data=cargardata.load_noticias(dirnoticias)
            if (data.size>0):
                with open(path_modelo, 'rb') as f:
                    model = pickle.load(f)
                    violencia,genericas=appmodel.evaluar(data,model) 
                    if violencia and genericas:
                        #self.setEnabled(False)
                        _ventanaclasificar=Ventana_Clasifica(nombre_modelo)
                        _ventanaclasificar.con_tabla(violencia,genericas)
                        _ventanaclasificar.show_win()
                        
   
                    else :
                        QMessageBox.about(self, "ERROR", "Error al clasificar las noticias")    
            else: 
                QMessageBox.about(self, "ERROR", "Error al cargar los archivos a clasificar")
        else:
            QMessageBox.about(self, "ERROR", "No has seleccionado ninguna carpeta para clasificar")

class Ventana_Clasifica(QWidget):
     #Método constructor de la clase
     def __init__(self,nombre):
      #Iniciar el objeto QMainWindow
      QWidget.__init__(self)
      #Cargar la configuración del archivo .ui en el objeto
      self.window
      self.nombre_modelo=nombre
      self.genericas=[]
      self.violencia=[]
      self.table_model_violencia=0
      self.setPalette(pallet(902,683))
      #self.ventana_Index=Ventana
      self.path_clasificar=""
      self.window =uic.loadUi("Ventana_Clasificacion.ui", self)
      
      self.setWindowTitle("Clasificado por el modelo "+ self.nombre_modelo)
      self.btt_Reentreno.clicked.connect(self.reentrenar)
      self.btt_Guardar_Noticias.clicked.connect(self.guardar)
     def show_win(self):
         self.window.show()
     def guardar(self):
         file = str(QFileDialog.getExistingDirectory(self, "Select Directory")) 
         if file:
             os.makedirs(file+os.path.sep+"Violencia")
             vio=cargardata.guardar_Noticias(file+os.path.sep+"Violencia"+os.path.sep+"VG",appmodel.CargarNoticias(self.violencia))
             os.makedirs(file+os.path.sep+"Genericas")
             gen=cargardata.guardar_Noticias(file+os.path.sep+"Genericas"+os.path.sep+"Gen",appmodel.CargarNoticias(self.genericas),)
             if(vio and gen):
                 QMessageBox.about(self, "Informacion", "Noticias guardadas")
             else :
                  QMessageBox.about(self, "ERROR", "Error al guardar las noticias")
     def reentrenar(self):
         noticias=appmodel.CargarNoticias(self.violencia)
         for i in noticias:
             if(not cargardata.Agregar_TXT(self.nombre_modelo, "VG", i)):
                 QMessageBox.about(self, "ERROR", "Error al cargar los archivos a clasificar")
         noticias=appmodel.CargarNoticias(self.genericas)
         for i in noticias:
             if(not cargardata.Agregar_TXT(self.nombre_modelo, "General", i)):
                 QMessageBox.about(self, "ERROR", "Error al cargar los archivos a clasificar")
         PATH='.'+os.path.sep+'modelos'+os.path.sep+self.nombre_modelo+'.txt'
         dirname0=cargardata.obtener_path_reentrenamiento(self.nombre_modelo)
         data,target_names,target=cargardata.load_files(dirname0)
         modelo = model.crearModelo(data,target,target_names, outpath=PATH)
         if(modelo):
             QMessageBox.about(self, "Correcto", "Reentrenamiento correcto")
            
     def cellClick_Vg(self,row,col):
        if(col==2):
            elec=QMessageBox.question(self, "Informacion", "Quiere previsualizar la noticia",QMessageBox.Yes |QMessageBox.No)
            if elec==QMessageBox.Yes:
                titulo=self.tbl_Vg.item(row,1).text()
                desc=self.tbl_Vg.item(row,col).text()
                fecha=self.tbl_Vg.item(row,0).text()
                noticia=Noticia.Noticia(titulo,desc,fecha)
                _ventanapreviw=Ventana_Previuw(noticia)
                _ventanapreviw.show_win()
        
        else:
            elec=QMessageBox.question(self, "Informacion", "Quiere reclasificar la noticia ",QMessageBox.Yes |QMessageBox.No)
            if elec==QMessageBox.Yes:
                genericas=[]
                violencia=[]
                violencia,genericas=appmodel.reclasificar(self.violencia,self.genericas,row)
                self.tbl_Vg.setColumnCount(0)
                self.tbl_Vg.setRowCount(0)
                self.con_tabla(violencia,genericas)
     def cellClick_Nvg(self,row,col):
           if(col==2):
                elec=QMessageBox.question(self, "Informacion", "Quiere previsualizar la noticia",QMessageBox.Yes |QMessageBox.No)
                if elec==QMessageBox.Yes:
                    titulo=self.tbl_Nvg.item(row,1).text()
                    desc=self.tbl_Nvg.item(row,col).text()
                    fecha=self.tbl_Nvg.item(row,0).text()
                    noticia=Noticia.Noticia(titulo,desc,fecha)
                    _ventanapreviw=Ventana_Previuw(noticia)
                    _ventanapreviw.show_win()
           else:
               elec=QMessageBox.question(self, "Informacion", "Quiere reclasificar la noticia ",QMessageBox.Yes |QMessageBox.No)
               if elec==QMessageBox.Yes:
                    genericas=[]
                    violencia=[]
                    genericas, violencia=appmodel.reclasificar(self.genericas,self.violencia,row)
                    self.tbl_Vg.setColumnCount(0)
                    self.tbl_Vg.setRowCount(0)
                    self.con_tabla(violencia,genericas)      
     def con_tabla(self,violencia,genericas):
      self.violencia=violencia
      self.genericas=genericas
      #añadirle las cabeceras
      header = ["Fecha","Titulo","Descripcion"]
      #cargamos la tabla de violencia
      noticias=appmodel.CargarNoticias(self.violencia)
      
      data=appmodel.contenido_tabla(noticias)
      self.tbl_Vg.setColumnCount(3)
      self.tbl_Vg.setHorizontalHeaderLabels(header)
      self.tbl_Vg.setRowCount(len(data))
      #Añadimos el controlador
      self.tbl_Vg.cellClicked.connect(self.cellClick_Vg)
      r=0
      for i in data:
        c=0  
        for e in i:
            item=QTableWidgetItem(e)
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tbl_Vg.setItem(r,c, item)
            c=c+1
        r=r+1
      head = self.tbl_Vg.horizontalHeader()
      head.setSectionResizeMode(QHeaderView.Stretch)
      head.setStretchLastSection(True)  
    #cargamos la tabla de genericas
      noticias=appmodel.CargarNoticias(self.genericas)
      
      data=appmodel.contenido_tabla(noticias)
      self.tbl_Nvg.setColumnCount(3)
      self.tbl_Nvg.setHorizontalHeaderLabels(header)
      self.tbl_Nvg.setRowCount(len(data))
      self.tbl_Nvg.cellClicked.connect(self.cellClick_Nvg)
      r=0
    
      for i in data:
        c=0  
        for e in i:
            item=QTableWidgetItem(e)
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tbl_Nvg.setItem(r,c,item )
            c=c+1
        r=r+1
      head = self.tbl_Nvg.horizontalHeader()
      head.setSectionResizeMode(QHeaderView.Stretch)
      head.setStretchLastSection(True)
     
      #self.table_model_violencia = MyTableModel.__init__(self,data, header, self)
      #self.tbl_Vg.setModel(self.table_model_violencia)
       
class Ventana_Previuw(QWidget):
     #Método constructor de la clase
     def __init__(self,noticia):
      #Iniciar el objeto QMainWindow
      QWidget.__init__(self)
      #Cargar la configuración del archivo .ui en el objeto
      #self.ventana_Index=Ventana
      self.noticia=noticia
      self.path_clasificar=""
      self.window
      tit=""
      desc=""
      window=uic.loadUi("Preview.ui", self)
      self.setWindowTitle("Visualizar una noticia")
      self.window=window
      descrip=self.splitStringMax(self.noticia.descripcion,120)
      for i in descrip:
          desc=desc+"\n"+i
      titulo=self.splitStringMax(self.noticia.descripcion,100)
      for i in titulo:
          tit=tit+"\n"+i
      self.window.lbl_Titulo.setText(tit);
      self.window.lbl_Descripcion.setText(desc);
      self.window.lbl_Fecha.setText(self.noticia.fecha)
     def show_win(self):
         self.window.show()
     def splitStringMax(self,si, limit):
        ls = si.split()
        lo=[]
        st=''
        ln=len(ls)
        if ln==1:
            return [si]
        i=0
        for l in ls:
            st+=l
            i+=1
            if i <ln:
                lk=len(ls[i])
                if (len(st))+1+lk < limit:
                    st+=' '
                    continue
            lo.append(st);st=''
        return lo
#Instancia para iniciar una aplicación
app = QApplication(sys.argv)
#Crear un objeto de la clase
_ventana = Ventana_Principal()
#Mostra la ventana
_ventana.show()
#Ejecutar la aplicación
app.exec_()
