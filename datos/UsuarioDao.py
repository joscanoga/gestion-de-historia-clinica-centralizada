import json


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
        consulta = "SELECT nombre , email ,telefono, direccion, fecha_nacimieto, verificaion, cambio  FROM {} WHERE id= '{}'   ".format(data["tipo"], str(data["id"]))
        cursor.execute(consulta)
        registros = cursor.fetchall()

        dato=registros[0]
        id=data["id"]
        datos='{"datos":{ "id":"'+str(id)+'","nombre" : "'+str(dato[0])+'","email":"'+str(dato[1])+'","telefono":"'+str(dato[2])+'","direccion":"'+str(dato[3])+'", "fecha_nacimiento":"'+str(dato[4])+'","verificacion" :"'+str(dato[5])+'","cambio" :"'+str(dato[6])+'"}}'
        return datos

    @classmethod
    def datosHospital(cls, **data):
        cursor = Conexion.obtenerCursor()
        consulta = "SELECT nombre , email ,telefono, direccion, servicios,verificaion, cambio  FROM {} WHERE id= '{}'   ".format(
            data["tipo"], data["id"])
        cursor.execute(consulta)
        registros = cursor.fetchall()

        dato = registros[0]
        id = data["id"]
        s=list(map(lambda x: x.rstrip(),dato[4].split()))
        datos = '{"datos":{ "id":"' + str(id) + '","nombre" : "' + str(dato[0]) + '","email":"' + str(dato[1]) + '","telefono":"' + str(dato[2]) + '","direccion":"' + str(dato[3]) + '", "servicios":"' + str(dato[4]) + '","verificacion" :"'+str(dato[5])+'","cambio" :"'+str(dato[6])+'"}}'
        return datos

    @classmethod
    def datosMedico(cls, **data):
        cursor = Conexion.obtenerCursor()
        consulta = "SELECT nombre , email ,telefono, id_hospital, verificaion ,cambio FROM {} WHERE id= '{}'   ".format(
            data["tipo"], str(data["id"]))
        cursor.execute(consulta)
        registros = cursor.fetchall()

        dato = registros[0]
        id = data["id"]
        #se consulta  nombre del hospital al que pertenece el medico
        nombre=json.loads(UsuarioDao.datosHospital(id=dato[3],tipo="hospital"))["datos"]["nombre"]
        datos = '{"datos":{ "id":"' + id + '","nombre" : "' + dato[0] + '","email":"' + dato[1] + '","telefono":"'+dato[2] + '","id_hospital":"' + dato[3] + '", "nombre_hospital":"' + nombre + '","verificacion" :"'+str(dato[4])+ '","cambio" :"'+str(dato[5])+'"}}'
        return datos
    @classmethod
    def obs(cls,**data):
        global registros
        datos="[ "
        cursor = Conexion.obtenerCursor()
        if data["tipo"]=="paciente":
            consulta = "SELECT pac.nombre, pac.id,obs.id,obs.obserbacion,obs.especialidad,med.id, med.nombre,hos.nombre FROM paciente AS pac INNER JOIN observacion AS obs ON obs.paciente=pac.id INNER JOIN medico as med on obs.medico=med.id INNER JOIN hospital as hos on hos.id=med.id_hospital WHERE pac.id='{}';".format( str(data["id"]))
            cursor.execute(consulta)
            registros = cursor.fetchall()
        elif data["tipo"]=="medico":
            consulta = "SELECT pac.nombre, pac.id,obs.id,obs.obserbacion,obs.especialidad,med.id, med.nombre,hos.nombre FROM paciente AS pac INNER JOIN observacion AS obs ON obs.paciente=pac.id INNER JOIN medico as med on obs.medico=med.id INNER JOIN hospital as hos on hos.id=med.id_hospital WHERE med.id='{}';".format( str(data["id"]))
            cursor.execute(consulta)
            registros = cursor.fetchall()
        elif data["tipo"]=="hospital":
            consulta = "SELECT pac.nombre, pac.id,obs.id,obs.obserbacion,obs.especialidad,med.id, med.nombre,hos.nombre FROM paciente AS pac INNER JOIN observacion AS obs ON obs.paciente=pac.id INNER JOIN medico as med on obs.medico=med.id INNER JOIN hospital as hos on hos.id=med.id_hospital WHERE hos.id='{}';".format( str(data["id"]))
            cursor.execute(consulta)
            registros = cursor.fetchall()

        for dato in registros:
            datos += '{ "nombre_paciente":"' + str(dato[0]) + '","id_paciente" : "' + str(dato[1]) + '", "id_observacion":"' + str(dato[2])+'","observacion":"' + str(dato[3]) + '","especialidad":"'+str(dato[4])+ '","id_medico":"' + str(dato[5]) + '", "nombre_medico":"' + str(dato[6]) +'", "nombre_hospital":"' + str(dato[7])+ '"},'
        return datos[:-1]+"]"

