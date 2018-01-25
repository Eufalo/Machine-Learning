class Noticia:
    
    def __init__ (self, nuevoTitulo, nuevaDescripcion, nuevaFecha):
        self.titulo=nuevoTitulo
        self.descripcion=nuevaDescripcion
        self.fecha =nuevaFecha

    def titulo (self):
        return self.titulo
    def descripcion (self):
        return self.descripcion
    def fecha (self):
        return self.fecha