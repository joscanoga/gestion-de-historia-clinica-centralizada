class Usuario:
    def __init__(self, identificacion=None, email=None, telefono=None, contrasena=None):
        self.__contrasena = contrasena
        self.__telefono = telefono
        self.__email = email
        self.__identificacion = identificacion
        self.verificaion=False

    def get_identificacion(self):
        return self.__identificacion
    def get_telefono(self):
        return self.__telefono
    def get_email(self):
        return self.__email
    def get_contrasena(self):
        return self.__contrasena
    def set_identificacion(self,identificacion):
        self.__identificacion=identificacion
    def set_telefono(self,telefono):
        self.__telefono=telefono


