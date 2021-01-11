import json

from usurarios import Paciente as p, Hospital
from datos.Conexion import Conexion


class UsuarioDao:
    @classmethod
    def registrarUsusario(cls,tipo,datos):
        if tipo == "paciente":
            print()
        # crear usuario tipo paciente
        elif tipo=="Hospital":
            print()
            #crear usuario tipo hospital
        else:
            print()
            #marcar error tipo de usuario incorecto
    @classmethod
    def autentificarUsuario(cls,**data):
        cursor=Conexion.obtenerCursor()
        consulta="SELECT * FROM {} WHERE id= '{}' and contrasena='{}'  ".format(data["tipo"],data["id"],data["password"])
        cursor.execute(consulta)
        registros=cursor.fetchall()

        if (len(registros))==1:
            return True

    @classmethod
    def datosPacientes(cls,**data):
        cursor = Conexion.obtenerCursor()
        consulta = "SELECT nombre , email ,telefono, direccion, fecha_nacimiento FROM {} WHERE id= '{}'   ".format(data["tipo"], str(data["id"]))
        cursor.execute(consulta)
        registros = cursor.fetchall()

        dato=registros[0]
        id=data["id"]
        datos='{"datos":{ "id":"'+str(id)+'","nombre" : "'+str(dato[0])+'","email":"'+str(dato[1])+'","telefono":"'+str(dato[2])+'","direccion":"'+str(dato[3])+'", "fecha_nacimiento":"'+str(dato[4])+'"}}'
        return datos

    @classmethod
    def datosHospital(cls, **data):
        cursor = Conexion.obtenerCursor()
        consulta = "SELECT nombre , email ,telefono, direccion, servicios FROM {} WHERE id= '{}'   ".format(
            data["tipo"], data["id"])
        cursor.execute(consulta)
        registros = cursor.fetchall()

        dato = registros[0]
        id = data["id"]
        s=list(map(lambda x: x.rstrip(),dato[4].split()))
        datos = '{"datos":{ "id":"' + str(id) + '","nombre" : "' + str(dato[0]) + '","email":"' + str(dato[1]) + '","telefono":"' + str(dato[2]) + '","direccion":"' + str(dato[3]) + '", "servicios":"' + str(dato[4]) + '"}}'
        return datos

    @classmethod
    def datosMedico(cls, **data):
        cursor = Conexion.obtenerCursor()
        consulta = "SELECT nombre , email ,telefono, id_hospital FROM {} WHERE id= '{}'   ".format(
            data["tipo"], str(data["id"]))
        cursor.execute(consulta)
        registros = cursor.fetchall()

        dato = registros[0]
        id = data["id"]
        nombre=json.loads(UsuarioDao.datosHospital(id=dato[3],tipo="hospital"))["datos"]["nombre"]
        datos = '{"datos":{ "id":"' + id + '","nombre" : "' + dato[0] + '","email":"' + dato[1] + '","telefono":"'+dato[2] + '","id_hospital":"' + dato[3] + '", "nombre_hospital":"' + nombre + '"}}'
        return datos

