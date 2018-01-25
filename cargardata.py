from os.path import join
import glob
import os
import re
import numpy as np
import Noticia

def obtener_path(dirname0):
    
    #Creamos 3 arrays:
         #Target es la matriz que muestra el boleano de si pertenece a una categoria o a otra.
         #Target names es el nombre de nuestras categorias
         #filenames contiene el path completo de los archivos
       
    target = []
    target_names = []
    filenames = []
    
    #Obtenemos las subcarpetas que hay en el path dirname0(Categorias)
    folders = os.listdir(dirname0)
    #Enumeramos las subcarpetas
    for label, folder in enumerate(folders):
        
        if(folder=='.DS_Store'):
            print("Carpeta no necesaria")
        else:
            #Agrega la categoria de la carpeta en la que nos encontremos
            target_names.append(folder)
            
            #Aceddemos a la subcarpeta en cuestion (VG o general)
            folder_path = join(dirname0, folder)
            
            #Se junta el path de la subcarpeta a cualquier archivo .txt
            documents = [join("", d)
                         for d in sorted(glob.glob(folder_path+os.path.sep + '*.txt'))]
            
            
            #Une las matrices de las categorias
            target.extend(len(documents) * [label])
            
            
            #Agregamos el path de cada archivo txt a filenames[].
            filenames.extend(documents) 
    
    
    #Devolvemos la matriz de las categorias, y Nombre de las categorias, Path al los archivos 
    return target, target_names, filenames

    
  
 
#Funcion para cargar los archivos  para entrener al modelo  
def load_files (dirname0, description=None, categories=['General', 'VG'],
               load_content=True, shuffle=False, encoding='CP1252',
               decode_error='ignore', random_state=0):
        
    #Cargamos los datos de la funcion obtener_path
    target, target_names, filenames = obtener_path(dirname0)
    
        
    
    #Convertimos los datos a un array Numpy
    filenames = np.array(filenames)
    target = np.array(target)
    
    
    #Carga los archivos gracias al path que obtiene de filename
    if load_content:
        data = []
        for filename in filenames:
            
            #rb = lectura y escritura
            with open(filename, 'rb') as f:
                data.append(f.read())
        if encoding is not None:
            data = np.array([d.decode('CP1252', 'ignore') for d in data])
            
        #Gracias a los datos creamos un Bunch que es un 'diccionario'
        return data,target_names,target
       
    return data,target_names,target
    
#Funcion para cargar archivo para clasificar noticias
def load_noticias(dirnoticias,description=None,load_content=True, encoding='CP1252',
               decode_error='ignore', random_state=0):
    
        filenames= [join("", d)
                for d in sorted(glob.glob(dirnoticias+os.path.sep + '*.txt'))]

           
        #Carga los archivos gracias al path que obtiene de filename
        if load_content:
            data = []
            for filename in filenames:
                
                #rb = lectura y escritura
                with open(filename, 'rb') as f:
                    data.append(f.read())
            if encoding is not None:
                data = np.array([d.decode('CP1252', 'ignore') for d in data])
                
            #Gracias a los datos creamos un Bunch que es un 'diccionario'
            return data
           
        return data
def obtener_path_noticias_entrenamiento(path):
    categorias=os.listdir(path)
    return categorias
def obtener_path_reentrenamiento(modelo):
    directorio = '.'+ os.path.sep+'Entrenamiento'
    modelos = os.listdir(directorio)
    #buscamos en todos los modelos
    for m in modelos:
        if (m == modelo):
            #si encontramos el que buscamos lo agregammos al path
            directorio = directorio + os.path.sep+ m
            return directorio
def Obtener_Path_Entrenamiento (modelo, categoria):
 
    error = 'Error'
    
    
    directorio = '.'+ os.path.sep+'Entrenamiento'
    modelos = os.listdir(directorio)
    #buscamos en todos los modelos
    for m in modelos:
        if (m == modelo):
            #si encontramos el que buscamos lo agregammos al path
            directorio = directorio + os.path.sep+ m
            categorias = os.listdir(directorio)
            #buscamos en todas las categorias
            for c in categorias:
                if (c == categoria): 
                    #si encontramos la categoria que buscamos lo agregamos al path y lo devolvemos
                    directorio = directorio + os.path.sep+ c
                    return directorio
    return error        
def sortKeyFunc(s):
    file_text_name = os.path.splitext(os.path.basename(s))  #you get the file's text name without extension
    file_last_num = os.path.basename(file_text_name[0]).split('_')  #you get three elements, the last one is the number. You want to sort it by this number
    return int(file_last_num[1])
def Obtener_numero (directorio):
    
    archivos = [join("", d)
                         for d in glob.glob(directorio+os.path.sep + '*.txt')]
    #Obtengo el tipo de archivos (es una lista).
    #print(type(archivos))
    archivos.sort(key=sortKeyFunc)
    #coje el ultimo elemento de una lista
    ultimo_nombre = archivos[-1]
    #separamos el nombre del archivo de la extension
    trozos = ultimo_nombre.split('.txt')
    #nos quedamos con el nombre del archivo
    ultimo_nombre = trozos[0]
    #me guardo en un auxiliar el nombre sin extension para obtener el nombre.
    Nombre = ultimo_nombre
    #eliminamos todo hasta llegar a un numero
    trozos = re.split("\D", ultimo_nombre) 
    #cojemos el ultimo elemento de la lista que sera nuestro numero
    numero = trozos[-1]
    #Sumamos +1 a nuestro numero
    numero = int(numero) + 1
    #Spliteamos hasta encontrar Strings
    trozos2 = re.split("\d", Nombre)
    #asignamos el nombre a la primeera posicion de la lista
    nombre = trozos2[0]
    
    return nombre, numero

def Agregar_TXT(modelo, categoria, noticia):
    directorio = Obtener_Path_Entrenamiento(modelo, categoria)
    if (directorio=="Error"):
        return False
    else:
        nombre,numero= Obtener_numero(directorio)
        numero = str(numero)
        archivo = nombre + numero + '.txt'
        #Creamos el fichero correspondiente en la carpeta que deseamos.
        file = open( archivo , "w")
        #Rellenamos el txt
        if file:
            file.write(noticia.titulo + '##'+noticia.descripcion + '##' + noticia.fecha)
            file.close()
            return True
        else :
            return False
def guardar_Noticias(path,noticia):
    a=0
    for i in range(len(noticia)):
        archivo = path+"_" +str(i)+ '.txt'
        #Creamos el fichero correspondiente en la carpeta que deseamos.
        file = open( archivo , "w")
        #Rellenamos el txt
        if file:
            file.write(noticia[i].titulo + '##'+noticia[i].descripcion + '##' + noticia[i].fecha)
            file.close()
            a=a+1
    if(a==len(noticia)):
        return True
    else: return False 
            