from abc import ABC, abstractmethod
from typing import List
from ..models import Product, ReportResult

class BaseProcessor(ABC):
    
    @property
    @abstractmethod
    def report_name(self) -> str:
        pass
    
    @abstractmethod
    def process(self, products: List[Product]) -> ReportResult:
        pass