# core/interfaces/email_repository.py
from abc import ABC, abstractmethod
from typing import Dict, List
from abc import ABC, abstractmethod
class logger_repository(ABC):
    @abstractmethod
    def log(self,endpoint, estado, resultado) -> None:
        pass
    
 