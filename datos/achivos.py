import openpyxl
from datos.Conexion import Conexion
def excel(**data):
    wb = openpyxl.Workbook()
    hoja = wb.active
    hoja.append(('nombre_paciente',"id_paciente","id_observacion", "observacion","especialidad","id_medico","nombre_medico","nombre_hospital"))
    cursor = Conexion.obtenerCursor()
    if data["tipo"] == "paciente":
        consulta = "SELECT pac.nombre, pac.id,obs.id,obs.obserbacion,obs.especialidad,med.id, med.nombre,hos.nombre FROM paciente AS pac INNER JOIN observacion AS obs ON obs.paciente=pac.id INNER JOIN medico as med on obs.medico=med.id INNER JOIN hospital as hos on hos.id=med.id_hospital WHERE pac.id='{}';".format(
            str(data["id"]))
        cursor.execute(consulta)
        registros = cursor.fetchall()
    elif data["tipo"] == "medico":
        consulta = "SELECT pac.nombre, pac.id,obs.id,obs.obserbacion,obs.especialidad,med.id, med.nombre,hos.nombre FROM paciente AS pac INNER JOIN observacion AS obs ON obs.paciente=pac.id INNER JOIN medico as med on obs.medico=med.id INNER JOIN hospital as hos on hos.id=med.id_hospital WHERE med.id='{}';".format(
            str(data["id"]))
        cursor.execute(consulta)
        registros = cursor.fetchall()
    elif data["tipo"] == "hospital":
        consulta = "SELECT pac.nombre, pac.id,obs.id,obs.obserbacion,obs.especialidad,med.id, med.nombre,hos.nombre FROM paciente AS pac INNER JOIN observacion AS obs ON obs.paciente=pac.id INNER JOIN medico as med on obs.medico=med.id INNER JOIN hospital as hos on hos.id=med.id_hospital WHERE hos.id='{}';".format(
            str(data["id"]))
        cursor.execute(consulta)
        registros = cursor.fetchall()
    for registro in registros:
        hoja.append(list(registro))
    wb.save('archivos/observaciones_{}.xlsx'.format(data["id"]))



