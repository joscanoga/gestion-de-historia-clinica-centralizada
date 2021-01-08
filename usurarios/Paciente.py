from usurarios.Usuarios import Usuario
class Paciente(Usuario):
    def __init__(self,identificacion,email,telefono,contrasena,nombre,direccion, fecha_nacimieto):
        super.__init__(identificacion,email,telefono,contrasena)
        self.__fecha_nacimieto = fecha_nacimieto
        self.nombre = nombre
        self.direccion = direccion

        def get_nombre(self):
            return self.__nombre

        def get_direccion(self):
            return self.__drieccion

        def set_nombre(self, nombre):
            self.__nombre = nombre

        def set_direccion(self, direccion):
            self.__direccion = direccion
        def set_fecha_nacimiento(self):
            return self.__fecha_nacimieto
