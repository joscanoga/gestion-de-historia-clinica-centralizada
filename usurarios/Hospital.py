from usurarios.Usuarios import Usuario
class Hospital(Usuario):
    def __init__(self,identificacion,email,telefono,contrasena,nombre,direccion, servicios):
        super().__init__(identificacion,email,telefono,contrasena)
        self.__servicios = servicios
        self.__direccion = direccion
        self.__nombre = nombre
    def get_nombre(self):
        return self.__nombre
    def get_direccion(self):
        return self.__drieccion
    def set_nombre(self,nombre):
        self.__nombre=nombre
    def set_direccion(self,direccion):
        self.__direccion=direccion
    def get_servicios(self):
        return self.__servicios
