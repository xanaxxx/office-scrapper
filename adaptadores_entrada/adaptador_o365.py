from O365 import Account
import datetime as dt
import pprint
import datetime as dt
from core.interfaces.email_repository import EmailRepository
import os
from dotenv import load_dotenv
from core.interfaces.logger_repository import logger_repository
#debe leerse por base de datos
load_dotenv()  # Cargar las variables de entorno desde el archivo .env
class adaptador_email_365(EmailRepository):
    def __init__(self,logger:logger_repository):
        self.account = None
        self.username = None
        self.credentials = {
            'clientID':os.getenv('clientIDO365'),
            'tenantID':os.getenv('tenantIDO365'),
            'clientSecret':os.getenv('clientSecretO365'),
            'username':os.getenv('UsernameO365'),
            'password':os.getenv('PasswordO365'),
            'host':os.getenv('HostO365')
        }
        self.logger = logger

    def login(self):

        try:
            print("--------------------CREDENTIALS",self.credentials)
            clientID = self.credentials['clientID']
            clientSecret = self.credentials['clientSecret']
            tenantID = self.credentials['tenantID']
            username = self.credentials['username']
            authority = 'https://login.microsoftonline.com/{}'.format(tenantID)
            #scopes =['https://graph.microsoft.com/.default']
            credentials = (clientID, clientSecret)
            account = Account(credentials, auth_flow_type='credentials', tenant_id=tenantID)
            if account.authenticate():
                self.account = account
                self.username = username
                return True
            else:
                print('Authentication failed')
                self.logger.log('o365', 'Error during authentication: ', 'Authentication failed')
                return False
                
        except Exception as e:
            print('Error during authentication:', e)
            self.logger.log('o365', 'Error during authentication: ', str(e))
            return 'AUTENTICACION FALLIDA, REVISAR CREDENCIALES'+ str(e)
    


    """
    Obtiene los correos electrónicos del día de hoy de la bandeja de entrada del usuario autenticado en Office 365.
    Esta función autentica al usuario (si no está autenticado), accede a la bandeja de entrada y recolecta los correos recibidos desde el día actual, incluyendo sus adjuntos y metadatos relevantes.
    Returns:
        dict: Un diccionario con dos claves:
            - "content": Lista de diccionarios, cada uno representando un correo con sus detalles (ID, remitente, asunto, fecha, categorías, marcaciones y adjuntos).
            - "ids": Lista de IDs de los correos recolectados.
        str: Mensaje de error si ocurre algún problema durante la autenticación o la obtención de correos.
    Raises:
        Exception: Si ocurre un error durante la autenticación o la obtención de los correos.
    # Esta función obtiene los correos electrónicos recientes de la bandeja de entrada de un usuario autenticado en Office 365.
    """
    def obtener_correos(self):
        try:
            if not self.account and not self.login():
                return 'ERROR AL LOGEARSE, POR FAVOR REVISAR LAS CREDENCIALES'
            recolected_data ={}
            recolected_ids=[]
            all_data = []
            #definimos los periodos de tiempo, valido los de la última hora.
            print('Authenticated! from getting_email')
            mailbox = self.account.mailbox(resource=self.username)
            inbox = mailbox.inbox_folder() #Bandeja de entrada
            start = dt.date.today()
            query = mailbox.new_query()
            query = query.on_attribute('created_date_time').greater_equal(start)
            #query = query.on_attribute('from').contains('m.sebastian@montechelo.com.co') #De
            #no limit si queremos limitarlos agregar el parametro limit
            for msg in inbox.get_messages(download_attachments=True,query=query):
                
                attachements = msg.attachments
                if msg.flag.to_api_data()['flagStatus']== 'flagged':
                
                    recolected_ids.append(msg.object_id)   
                    all_data.append({
                    'id_conversacion': msg.conversation_id,
                    'id_correo': msg.object_id,
                    'remitente': msg.sender.address+" "+msg.sender.name,
                    'asunto': msg.subject,
                    'fecha_recibido': msg.received.isoformat(),
                    'categorias': str(msg.categories),
                    'marcaciones': str(msg.flag.to_api_data()),
                    'adjuntos': attachements,
                    
                    })

                recolected_data={
                    "content": all_data,
                    "ids":recolected_ids
                }
            
            return recolected_data
        except Exception as e:
            print('Error during authentication:', e)
            self.logger.log('o365', 'Error during emails: ', str(e))
            return 'ERROR AL OBTENER LOS EMAILS, POR FAVOR REVISAR EL SIGUIENTE ERROR'+ str(e)
        


    """
        Obtiene y guarda los archivos adjuntos de una lista de correos electrónicos.
        Esta función procesa una lista de diccionarios (final_array), donde cada diccionario representa un correo electrónico y puede contener una lista de archivos adjuntos. 
        Para cada adjunto válido (con extensiones permitidas), guarda el archivo en un directorio específico basado en la fecha de recepción y el remitente, y construye una estructura 
        que asocia los IDs de correo con las rutas de los archivos descargados. Si no hay adjuntos válidos, se agrega "NO-DATA" para ese correo, esto aplica cuando hay correos que no tienen adjuntos validos o simplemente no traen adjuntos.
        Args:
            final_array (list): Lista de diccionarios, cada uno representando un correo electrónico con posibles adjuntos.
        Returns:
            list: Lista de diccionarios, cada uno con el ID del correo y las rutas de los archivos adjuntos descargados en un arreglo convertido en string.
                  Si ocurre un error, retorna un string con el mensaje de error.
        # Esta función obtiene los adjuntos de los correos, los guarda en disco y retorna las rutas asociadas a cada correo.
    """



    def obtener_adjuntos(self,final_array):
   
        try:
            #creo el path absoluto para guardar los adjuntos
            base_dir = os.path.dirname(os.path.abspath(__file__))
            dict_adjuntos={}
            print("👉👉👉👉👉👉👉👉👉👉👉WHAT I RECIVE",final_array)
            #recorro todo el objeto
            for i in final_array:
                adjuntos=i.get('adjuntos')
                #obtengo los adjuntos dentro del objeto  final_array y dentro de la clave adjuntos
                print("obteniendo adjuntos🧐🧐🧐🧐🧐🧐🧐",i )
                #si adjuntos existe y tiene algo dentro
                if adjuntos and len(adjuntos)>0:
                    for archivo in adjuntos:
                        print("🍟🍟🍟🍟🍟🍟🍟🍟archivo",archivo.name,"--------------------",i.get('remitente'))
                        new_date=i.get('fecha_recibido').replace(':','-')
                        adjuntos_dir = os.path.abspath(os.path.join(base_dir, "..", "adjuntos/"+new_date+'-'+i.get('remitente')))
                        # Use os.makedirs() to create the directory and any missing parent directories
                        if '.'in str(archivo.name) and  str(archivo.name).split('.')[1] in ['pdf', 'docx', 'doc', 'xlsx', 'xls', 'ppt','jpg','png']:
                            try:
                                print("ENTRO AL TRY----------------------")
                                if not os.path.exists(adjuntos_dir):
                                    os.makedirs(adjuntos_dir)
                                print("CREACION DEL DI")
                                print(f"Directory '{adjuntos_dir}' created successfully.")
                                #print("extension",archivo.extension)
                                descarga_ruta=os.path.join(adjuntos_dir, archivo.name)
                                
                                archivo.save(adjuntos_dir)
                                last_id = i.get('id_correo')
                                #si el último id no esta en el diccionario le asigno una lista vacia
                                if last_id not in dict_adjuntos:
                                    dict_adjuntos[last_id] = []
                                #luego le agrego el valor
                                dict_adjuntos[last_id].append(str(descarga_ruta))
                                print("descargado", descarga_ruta)
                                
                            except FileExistsError:
                                print(f"Directory '{adjuntos_dir}' already exists.")
                            except Exception as e:
                                print(f"An error occurred: {e}")
                        else:
                            last_id = i.get('id_correo')
                            if last_id not in dict_adjuntos:
                                dict_adjuntos[last_id] = []
                            dict_adjuntos[last_id].append("NO-DATA-VALIDA")
                else:
                    last_id = i.get('id_correo')
                    if last_id not in dict_adjuntos:
                        dict_adjuntos[last_id] = []
                    dict_adjuntos[last_id].append("")           
                print("----------------------------------------adjuntos",dict_adjuntos)
                #del i['adjuntos']
            correos_files = [
            {
                "id_correo": id_correo,
                "archivos": str(rutas)  # convierte lista a string con formato de lista
            }
            for id_correo, rutas in dict_adjuntos.items()
             ]
            
            return correos_files

                            
        except Exception as e:
            print('Error during process:', e)
            self.logger.log('o365', 'Error during getting emails: ', str(e))
            return 'ERROR AL OBTENER LOS EMAILS, POR FAVOR REVISAR EL SIGUIENTE ERROR'+ str(e)
        