
from sqlalchemy import Boolean, Column , ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from database import  db







#######################################################################
class Paciente(db.Model):
    __tablename__ = "paciente"
    id = db.Column(String(12), primary_key=True)
    contrasena = Column(String(100), nullable=False)
    telefono = Column(String(15), nullable=False)
    email = Column(String(50), nullable=False)
    verificaion = Column(Boolean, default=False, nullable=False)
    cambio = Column(Boolean, default=False, nullable=False)
    fecha_nacimieto = Column(String(50), nullable=False)
    nombre = Column(String(50),nullable=False)
    direccion =Column(String(50),nullable=False)
    """
    @property
    def contrasena(self):
        raise AttributeError('password is not a readable attribute')

    @contrasena.setter
    def contrasena(self, password):
        self.contrasena = generate_password_hash(password)

    def verificar_contrasena(self, password):
        return check_password_hash(self.password_hash, password)
    """
########################################################################
class Hospital(db.Model):
    __tablename__ ="hospital"
    id = db.Column(String(12), primary_key=True)
    contrasena = Column(String(100), nullable=False)
    telefono = Column(String(15), nullable=False)
    email = Column(String(50), nullable=False)
    verificaion = Column(Boolean, default=False, nullable=False)
    cambio = Column(Boolean, default=False, nullable=False)
    servicios = Column(String(100),nullable=False)
    direccion = Column(String(50),nullable=False)
    nombre = Column(String(50),nullable=False)



#####################################################################
class Medico(db.Model):
    __tablename__ ="medico"
    id = db.Column(String(12), primary_key=True)
    contrasena = Column(String(100), nullable=False)
    telefono = Column(String(15), nullable=False)
    email = Column(String(50), nullable=False)
    verificaion = Column(Boolean, default=False , nullable=False)
    cambio = Column(Boolean, default=False,  nullable=False)
    id_hospital = Column(String(12),ForeignKey("hospital.id"),nullable=False)
    nombre =Column(String(50),nullable=False)




#############################################################################
class Observacion(db.Model):
    __tablename__ ="observacion"
    id = Column(Integer,primary_key=True)
    obserbacion = Column(String(500),nullable=False)
    paciente = Column(String,ForeignKey("paciente.id"),nullable=False)
    medico = Column(String(12),ForeignKey("medico.id"),nullable=False)
    especialidad=Column(String(50),nullable=False)