# -*- coding: utf-8 -*-

from cx_Freeze import setup, Executable
 
setup(name="ClasificadorVG", #el nombre de tu programa
 version="1.0", 
 description="descripcion", #una descripcion 
 author="Cejas", #aqu� va tu nombre 
 author_email="email del autor", # tu correo
 url="url del proyecto", #url del proyecto
 license="tipo de licencia", #tipo de licencia
 scripts=["controlador_Index.py"], #aqu� va el nombre del script a transformar a ejecutable
 console=["controlador_Index.py"], #aqu� tambi�n
 options={"py2exe": {"bundle_files": 1}}, 
 zipfile=None,
)