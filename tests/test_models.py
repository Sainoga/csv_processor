import pytest
from pathlib import Path

from src.csv_processor.models import Product, CSVReader
from src.csv_processor.exceptions import InvalidCSVFormatError


class TestProduct:
    
    def test_from_dict_valid(self):
        data = {
            "name": "test product",
            "brand": "test brand", 
            "price": "100.0",
            "rating": "4.5"
        }
        
        product = Product.from_dict(data)
        
        assert product.name == "test product"
        assert product.brand == "test brand"
        assert product.price == 100.0
        assert product.rating == 4.5
    
    @pytest.mark.parametrize("invalid_data,expected_error", [
        ({"brand": "test", "price": "100", "rating": "4.5"}, "name"),  # Missing name
        ({"name": "test", "price": "100", "rating": "4.5"}, "brand"),  # Missing brand
        ({"name": "test", "brand": "test", "rating": "4.5"}, "price"),  # Missing price
        ({"name": "test", "brand": "test", "price": "100"}, "rating"),  # Missing rating
        ({"name": "test", "brand": "test", "price": "invalid", "rating": "4.5"}, "price"),  # Invalid price
        ({"name": "test", "brand": "test", "price": "100", "rating": "invalid"}, "rating"),  # Invalid rating
    ])
    def test_from_dict_invalid(self, invalid_data, expected_error):
        with pytest.raises(InvalidCSVFormatError) as exc_info:
            Product.from_dict(invalid_data)
        
        assert expected_error in str(exc_info.value)


class TestCSVReader:
    
    def test_read_single_file_valid(self, sample_csv_file: Path):
        reader = CSVReader()
        products = reader._read_single_file(sample_csv_file)
        
        assert len(products) == 3
        assert all(isinstance(p, Product) for p in products)
        assert products[0].name == "iphone"
        assert products[0].brand == "apple"
        assert products[0].price == 999.0
        assert products[0].rating == 4.9
    
    def test_read_single_file_invalid_columns(self, invalid_csv_file: Path):
        reader = CSVReader()
        
        with pytest.raises(InvalidCSVFormatError) as exc_info:
            reader._read_single_file(invalid_csv_file)
        
        assert "must contain columns" in str(exc_info.value)
    
    def test_read_single_file_nonexistent(self):
        reader = CSVReader()
        
        with pytest.raises(FileNotFoundError):
            reader._read_single_file(Path("nonexistent.csv"))
    
    def test_read_multiple_files(self, sample_csv_file: Path, tmp_path: Path):
        # Create second file
        second_file = tmp_path / "second.csv"
        second_file.write_text("""name,brand,price,rating
product4,brand4,400,4.0
product5,brand5,500,5.0""")
        
        reader = CSVReader()
        products = reader.read_files([sample_csv_file, second_file])
        
        assert len(products) == 5  # 3 from first + 2 from second