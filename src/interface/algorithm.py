from abc import ABC, abstractmethod
from src.model.monitoring_db_model import MonitoringData 

class Algorithm(ABC):   
    @abstractmethod
    def run_algorithm(self, moniData:MonitoringData):
        """쓰레드가 돌릴 함수"""
        pass