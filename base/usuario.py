
class Usuario():
    def __init__(self,carnet,nombres,apellidos,contrasena,correo, creditos):
        self.carnet = carnet
        self.nombres = nombres
        self.apellidos = apellidos
        self.contrasena = contrasena
        self.correo = correo
        self.creditos = creditos

    def get_json(self):
        return {
            "carnet" : self.carnet,
            "nombres" : self.nombres,
            "apellidos" : self.apellidos,
            "contrasena": self.contrasena,
            "correo" : self.correo,
            "creditos" : self.creditos
        }

    def recuperar(self,contrasena):
        self.contrasena = contrasena