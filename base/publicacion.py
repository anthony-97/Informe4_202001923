class Publicacion():
    def __init__(self,autor,fecha,hora,curso,profesor, mensaje):
        self.autor = autor
        self.fecha = fecha
        self.hora = hora
        self.curso = curso
        self.profesor = profesor
        self.mensaje = mensaje
    
    def get_json(self):
        return {
            "autor" : self.autor,
            "fecha" : self.fecha,
            "hora" : self.hora,
            "curso" : self.curso,
            "profesor": self.profesor,
            "mensaje" : self.mensaje
        }