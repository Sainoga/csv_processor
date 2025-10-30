from dataclasses import dataclass
from typing import List, Optional
import csv
from pathlib import Path

from .exceptions import InvalidCSVFormatError

@dataclass
class Product:
    name: str
    brand: str
    price: float
    rating: float

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        try:
            return cls(
                name=data["name"],
                brand=data["brand"],
                price=float(data["price"]),
                rating=float(data["rating"]),
            )
        except (KeyError, ValueError) as e:
            raise InvalidCSVFormatError(f"Invalid product data: {data}, error: {e}")

@dataclass
class ReportResult:
    
    title: str
    headers: List[str]
    data: List[tuple]

class CSVReader:
    
    REQUIRED_COLUMNS = {"name", "brand", "price", "rating"}
    
    def read_files(self, file_paths: List[Path]) -> List[Product]:
        all_products = []
        
        for file_path in file_paths:
            products = self._read_single_file(file_path)
            all_products.extend(products)
            
        return all_products
    
    def _read_single_file(self, file_path: Path) -> List[Product]:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        products = []
        
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                dialect = csv.Sniffer().sniff(file.read(1024))
                file.seek(0)
            except csv.Error:
                dialect = csv.excel
            
            reader = csv.DictReader(file, dialect=dialect)
            
            if not self.REQUIRED_COLUMNS.issubset(reader.fieldnames or []):
                raise InvalidCSVFormatError(
                    f"CSV file {file_path} must contain columns: {self.REQUIRED_COLUMNS}"
                )
            
            for row_num, row in enumerate(reader, start=2):  # Start from 2 (header is row 1)
                try:
                    product = Product.from_dict(row)
                    products.append(product)
                except InvalidCSVFormatError as e:
                    raise InvalidCSVFormatError(
                        f"Error in {file_path}, row {row_num}: {e}"
                    ) from e
        
        return products