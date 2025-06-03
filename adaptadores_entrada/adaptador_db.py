import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus
import pandas as pd
import pymysql
import numpy as np
from core.interfaces.db_repository import DB_Repositorio
from core.interfaces.logger_repository import logger_repository
def connect():
        try:
            load_dotenv()
            host = os.getenv("DATABD_HOST")
            user = os.getenv("DB_USER")
            key = os.getenv("DB_PASSWORD")
            port=os.getenv("DB_PORT")
            name=os.getenv("DB_NAME")
            escaped_key = quote_plus(key)
            
            print("GENERANDO LA CONEXIÓN CON MYSQL")
            print("👉RECOLECTANDO CREDENCIALES:")
            
            print("👉usuario:",user)
            print("👉key:", key)
            print("👉host:", host)
            
            engine = create_engine(
                f"mysql+pymysql://{user}:{escaped_key}@{host}:{port}/{name}"
            )
            print("engine CREADO✅", engine)
            return engine
        except pymysql.Error as e:
            return f"Error al conectarse a la base de datos: {e}"



class database_controller_adaptader (DB_Repositorio):
    #PENDIENTES AGREGAR EL DISPOSE CUANDO INSERTE EN BASE DE DATOS, YA NO NECESITO MAS EL MOTOR
    def __init__(self,logger:logger_repository):
        self.engine=connect();
        self.logger = logger

    
    def executor_query(self, query,params=None, isInsert=False):
        #para evitar repeticiones, uso dry, dont repeat yourself, por eso la ejecución de la clase se hace aparte
        try:
            
            print("Ejecutando consulta:", query)
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params)
                print("Consulta  ejecutada con éxito",result, "la consulta fue",query)
                if isInsert:
                    # Si es una inserción
                    connection.commit()
                    return result.rowcount
                data_obtenida=result.fetchall()
                return [id[0] for id in data_obtenida] if data_obtenida else []
                print("data obtenida",data_obtenida[0])
        except Exception as e:
            self.logger.log('o365', 'Error during executing query: ', str(e))
            print(f"Error executing query: {e}")
            return None
        finally:
            self.engine.dispose() 

    def obtener_fecha(self):
        try:
            query='SELECT NOW();'
            result=self.executor_query(query,None)
            return result
            
        except Exception as e:
            self.logger.log('o365', 'Error during obtaining current date: ', str(e))
            print(f"Error executing query: {e}")
            return None
    def obtener_todos_ids(self, actual_fecha=None):
        try:
            return self.executor_query("SELECT id_correo FROM correos where DATE(created_at)= :actual_fecha;",{"actual_fecha": actual_fecha},False)
            
            
        except Exception as e:
            print(f"Error executing query: {e}")
            self.logger.log('o365', 'Error during obtaining email IDs: ', str(e))
            return None

    def guardar_correos(self, correos_datos ):
        print("🧐🧐🧐🧐🧐guardando correos",correos_datos)
        try:
            # Convertir la lista de diccionarios a un DataFrame de pandas
            return self.executor_query("INSERT INTO correos ( id_conversacion,id_correo, remitente, asunto, fecha_recibido,categorias,marcaciones) VALUES (:id_conversacion,:id_correo, :remitente, :asunto, :fecha_recibido, :categorias,:marcaciones);",correos_datos, True)
            print("Correos guardados exitosamente")
        except Exception as e:
            self.logger.log('o365', 'Error during saving emails: ', str(e))
            print(f"Error al guardar los correos: {e}")

    def actualizar_rutas_adjuntos(self, correos_files):
        try:
            # Convertir la lista de diccionarios a un DataFrame de pandas
            return self.executor_query("UPDATE correos  SET archivos=:archivos WHERE id_correo=:id_correo;",correos_files, True)
        except Exception as e:
            print(f"Error al guardar los correos: {e}")
            self.logger.log('o365', 'Error during updating attachments paths: ', str(e))
            return None