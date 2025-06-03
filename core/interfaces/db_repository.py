# core/interfaces/repositorio.py
from abc import ABC, abstractmethod

class DB_Repositorio(ABC):
    @abstractmethod
    def guardar_correos(self, correos_datos):
        pass
    
    #@abstractmethod
    def obtener_por_id(self, id):
        pass
    @abstractmethod
    def obtener_fecha(self):
        pass

    @abstractmethod
    def obtener_todos_ids(self):
        pass

    #@abstractmethod
    def listar_todos(self):
        pass
    @abstractmethod
    def actualizar_rutas_adjuntos(self):
        pass