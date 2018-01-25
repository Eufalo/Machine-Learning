# -*- coding: utf-8 -*-
from anaconda_navigator.widgets.explorer import listdir

import os
import Noticia
import pickle
def reclasificar(arr1,arr2,index):
    #reordena el array2 con la noticia del index del arra1 eliminando esta de esta clasificacion
    arr=[]
    noticia=arr1[index]
    arr2.append(noticia)
    for i in arr1:
        if(noticia!=i):
            arr.append(i)
    return arr,arr2
def evaluar(x,model):
    predictions=[]
    violencia=[]
    genericas=[]
    z=0
    for i in model.predict(x):
        predictions.append(i)
    
    
    for i in predictions:
        if(int(i)==0):
            violencia.append(x[z])
        else :
            genericas.append(x[z])
        z=z+1
    return violencia, genericas 
def cargar_modelo(Path):
    with open(Path, 'rb') as f:
          model = pickle.load(f)
    return model
def existe_Path(PATH):
     if not os.path.exists(PATH):
         return False
     else : return True 
def obtener_modelos (directorio):
    modelos=[]
   
    for a in listdir(directorio) :
        if a.endswith(".txt") :
            dat=a.split(".")
            modelos.append(dat[0])
        
    return modelos
def contenido_tabla(noticias):

    tabla=[]
    for e in noticias:
        noty=[]
        noty.append(str(e.fecha))
        noty.append(str(e.titulo))
        noty.append(e.descripcion)
        
        tabla.append(noty)
    
    return tabla

def CargarNoticias(data):
    datos = []
    noticias =[]
  
    for noticia in data:
        datos = noticia.split('##')
        if(datos[0]):
            if(datos[1]):
                if(datos[2]):
                    noty = Noticia.Noticia(datos[0], datos[1],datos[2])
                else:
                    noty = Noticia.Noticia(datos[0], datos[1],"")
            else:
                noty = Noticia.Noticia(datos[0], "","")
        noticias.append(noty)
        
    return noticias
