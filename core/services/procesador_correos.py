from core.interfaces.db_repository import DB_Repositorio
from core.interfaces.email_repository import EmailRepository
from core.interfaces.logger_repository import logger_repository
from datetime import datetime, timedelta


class ProcesadorCorreos:

    #pendiente: si en el env detecta que esta en modo recuperación, entonces no aplica 

    #instancio las interfaces porque no me interesa saber que adaptador es el que me esta enviando los correos
    def __init__(self, email_adapter: EmailRepository, db_adapter: DB_Repositorio,logger: logger_repository):
        self.email_adapter = email_adapter
        self.db_adapter = db_adapter
        self.logger = logger 

    def ejecutar(self):
        try:
            correos = self.email_adapter.obtener_correos()
            db=self.db_adapter.obtener_todos_ids(self.obtener_fecha_actual())
            fecha=str(self.obtener_fecha_actual(type_date='Normal'))
            
            print("CORREOSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS:", correos)
            if correos =="ERROR AL LOGEARSE, POR FAVOR REVISAR LAS CREDENCIALES":
                self.logger.log('nucleo ejecutador', 'Error during emails: ', correos)
                return "HAY ERRORES POR FAVOR REVISAR"
            if correos['content'] == [] or correos['ids'] == []:
                self.logger.log('nucleo ejecutador', 'INFO  ', "Sin correos nuevos para insertar")
                return "No hay corres para insertar"
            #sino hay correos, entonces inserto los del día de hoy
            if db== []:
                if correos.get('content')==[] and correos.get('ids')==[]:
                    print("No hay correos nuevos para insertar.")
                    return "No hay correos nuevos para insertar."
                print("********************************OBTENIDOOOOOOOOOOOOOOOOOOOOOOOOO", correos)
                db_insertar=self.db_adapter.guardar_correos(correos.get('content'))
                self.email_adapter.obtener_adjuntos(correos.get('content'))
                self.db_adapter.actualizar_rutas_adjuntos(correos.get('content'))
            # si hay correo comparo db_in contra los ids de mis correos.
            #transformo en conjunto
            conjunto_bd = set(db)
            conjunto_correos = set(correos.get('ids'))
            #print("mis conjuntos", conjunto_bd,"                " ,conjunto_correos)
            #print("Correos obtenidos:", correos)
            #print("database got:", db)
            #print("mis fechas",self.obtener_fecha_actual())
            correos_a_insertar= conjunto_correos-conjunto_bd
            final_data=[]
            final_data_con_adjuntos=[]
            #print("Correos a insertar:", correos_a_insertar)
            #este si no hay correos es porque hay correos de hoy pero a la fecha actual no hay y ya están en bd por lo cual no inserta
            if not correos_a_insertar:
                self.logger.log('nucleo ejecutador', 'INFO  ', "De lo que hay en la base de datos y lo que hay en los correos, no hay nuevos correos para insertar.")
                print("--"+fecha+" No hay correos nuevos para insertar.")
                return "--"+fecha+" No hay correos nuevos para insertar."
            #buscar en el content por el id e insertar en base de datos
            #print("Correos a insertar:", correos.get("content"))
            for i in correos['content']:
                if i.get("id_correo") in correos_a_insertar:
                    print("encontrado",i)
                    final_data.append(i)
            print("FECHAAAAAAAAAAAAAAAAAAAAAs:", fecha)
            result=self.db_adapter.guardar_correos(final_data)
            returned_data=self.email_adapter.obtener_adjuntos(final_data)
            update=self.db_adapter.actualizar_rutas_adjuntos(returned_data)
            print("RESULTADO DE LA INSERCIÓN",update)
        except Exception as e:
            self.logger.log('nucleo ejecutador', 'Error during processing emails: ', str(e))
            print(f"Error al procesar los correos: {e}")
            return "Error al procesar los correos"
        #print("Correos insertados exitosamente")
        #si hay correos a insertar, entonces los inserto
    def obtener_fecha_actual(self,type_date='Normal'):
        # Obtener la hora actual
        ahora = datetime.now()
        if type_date=='Normal':
            actual_fecha = f"{ahora.year}-{ahora.month}-{ahora.day}"
            return actual_fecha
        elif type_date=='Detallada':
            actual_fecha_detallada = f"{ahora.year}-{ahora.month}-{ahora.day} {ahora.hour}:{ahora.minute}:{ahora.second}"    
            return actual_fecha_detallada