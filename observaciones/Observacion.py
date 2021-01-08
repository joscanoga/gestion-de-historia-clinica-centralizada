from usurarios.Medico import Medico
from usurarios.Paciente import Paciente
class Observacion:
    def __init__(self,id,medico, paciente ,obserbacion):
        self.id = id
        self.obserbacion = obserbacion
        self.paciente = paciente
        self.medico = medico
