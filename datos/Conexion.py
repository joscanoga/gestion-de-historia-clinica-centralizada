import psycopg2 as ps
from flask import url_for

from datos.logger import logger
import sys
import json

class Conexion:
    #los datos de conexion son recibidos por medio de un json
    __datos_conexion=json.load(open("datos/conexion.json"))
    __user = __datos_conexion["user"]
    __password = __datos_conexion["password"]
    __host = __datos_conexion["host"]
    __port = __datos_conexion["port"]
    __database = __datos_conexion["database"]
    __conexion = None
    __cursor=None


    @classmethod
    def obtenerConexion(cls):
        if cls.__conexion is None:
            try:
                cls.__conexion = ps.connect(user=cls.__user,
                                      password=cls.__password,
                                      host=cls.__host,
                                      port=cls.__port,
                                      database=cls.__database)
                logger.debug("Conexion exitosa: {}".format(cls.__conexion))
                return cls.__conexion
            except  Exception as e:
                logger.error("Error al conectar a la base de datos: {}".format(e))
                sys.exit()
        else:
            return cls.__conexion


    @classmethod
    def obtenerCursor(cls):
        if cls.__cursor is None:
            try:
                cls.__conexion=cls.obtenerConexion()
                cls.__cursor=cls.__conexion.cursor()
                logger.debug("se abrio el cursor exitosamente: {}".format(cls.__cursor))
                return cls.__cursor
            except Exception as e:
                logger.error("error al obtener el cursor: {}".format(e))
                sys.exit()
        else:
            return cls.__cursor



    @classmethod
    def cerrar(cls):
        if cls.__cursor is not None:
            try:
                cls.__cursor.close()
                #logger.debug("cursor cerrado corectamente")
            except Exception as e:
                logger.error("error al cerrar el cursor: {}".format(e))
        if cls.__conexion is not None:
            try:
                cls.__conexion.close()
                #logger.debug("conexion cerrada corectamente")
            except Exception as e:
                logger.error("error al cerrar la conexion: {}".format(e))
        logger.debug("se han cerrado los objetos de conexion")





