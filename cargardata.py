from os.path import join
import glob
import os
import numpy as np


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

    
  
 
#Funcion para cargar los archivos   
def load_files (dirname0, description=None, categories=['General', 'VG'],
               load_content=True, shuffle=False, encoding='UTF-8',
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
            data = [d.decode('UTF-8', 'ignore') for d in data]
            
        #Gracias a los datos creamos un Bunch que es un 'diccionario'
        return data,target_names,target
       
    return data,target_names,target
    


   