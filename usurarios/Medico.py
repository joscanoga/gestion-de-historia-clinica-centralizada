from usurarios.Usuarios import Usuario
class Medico(Usuario):
    def __init__(self,identificacion,email,telefono,contrasena,nombre, hospital):
        #relacionar con el hospital
        super.__init__(identificacion,email,telefono,contrasena)
        self.__hospital = hospital
        self.__nombre = nombre

        def get_nombre(self):
            return self.__nombre

        def get_direccion(self):
            return self.__drieccion

        def set_nombre(self, nombre):
            self.__nombre = nombre



