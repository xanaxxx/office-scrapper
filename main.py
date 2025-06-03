from adaptadores_entrada.adaptador_o365 import adaptador_email_365
from adaptadores_entrada.adaptador_db import database_controller_adaptader
from core.services.procesador_correos import ProcesadorCorreos
from adaptadores_entrada.adaptador_logger import AdaptadorLogger




#solo configuro la aplicación
def config_aplication():
    # Configuración de la aplicación
   logger = AdaptadorLogger() 
   email_adapter= adaptador_email_365(logger)
   db_adapter= database_controller_adaptader(logger)
   #retorno la clase para que se ejecute en el main
   return ProcesadorCorreos(email_adapter,db_adapter,logger)

#aqui si la ejecutamos
if __name__ == "__main__":
  control=config_aplication()
  control.ejecutar()