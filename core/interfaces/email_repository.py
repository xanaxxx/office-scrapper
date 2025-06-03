# core/interfaces/email_repository.py
from abc import ABC, abstractmethod
from typing import Dict, List
from abc import ABC, abstractmethod
class EmailRepository(ABC):
    @abstractmethod
    def login(self) -> bool:
        pass
    
    @abstractmethod
    def obtener_correos(self) -> Dict[list, List]:
        """Devuelve un diccionario con:
        - 'content': Lista de correos con sus datos
        - 'ids': Lista de IDs de correos
        """
        pass
    @abstractmethod
    def obtener_adjuntos(self) -> List:
        """Devuelve una lista de adjuntos"""
        pass