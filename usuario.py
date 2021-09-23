class Usuario():
    def __init__(self,carnet,nombres,apellidos,contrasena,correo):
        self.carnet = carnet
        self.nombres = nombres
        self.apellidos = apellidos
        self.contrasena = contrasena
        self.correo = correo

    def get_json(self):
        return {
            "carnet" : self.carnet,
            "nombres" : self.nombres,
            "apellidos" : self.apellidos,
            "contrasena": self.contrasena,
            "correo" : self.correo
        }

    def editar(self,carnet,nombres,apellidos,contrasena,correo):
        self.carnet = carnet
        self.nombres = nombres
        self.apellidos = apellidos
        self.contrasena = contrasena
        self.correo = correo


    def recuperar(self,contrasena):
        self.contrasena = contrasena