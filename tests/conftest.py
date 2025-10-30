import pytest
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from csv_processor.models import Product


@pytest.fixture
def sample_products() -> list[Product]:
    return [
        Product("iphone", "apple", 999.0, 4.9),
        Product("galaxy", "samsung", 1199.0, 4.8),
        Product("redmi", "xiaomi", 199.0, 4.6),
        Product("macbook", "apple", 1999.0, 4.7),
    ]


@pytest.fixture
def sample_csv_file(tmp_path: Path) -> Path:
    """Создает временный CSV файл для тестирования."""
    csv_content = """name,brand,price,rating
iphone,apple,999,4.9
galaxy,samsung,1199,4.8
redmi,xiaomi,199,4.6"""
    
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content)
    return file_path


@pytest.fixture
def invalid_csv_file(tmp_path: Path) -> Path:
    csv_content = """name,price,rating
iphone,999,4.9
galaxy,1199,4.8"""
    
    file_path = tmp_path / "invalid.csv"
    file_path.write_text(csv_content)
    return file_path