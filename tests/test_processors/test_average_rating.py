import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from csv_processor.processors.average_rating import AverageRatingProcessor
from csv_processor.models import Product


class TestAverageRatingProcessor:
    
    @pytest.fixture
    def processor(self):
        return AverageRatingProcessor()
    
    def test_report_name(self, processor):
        assert processor.report_name == "average-rating"
    
    def test_process_empty_list(self, processor):
        result = processor.process([])
        
        assert result.title == "average rating on brands"
        assert result.headers == ["Brand", "Average rating"]
        assert result.data == []
    
    def test_process_single_brand(self, processor):
        products = [
            Product("p1", "apple", 100, 4.0),
            Product("p2", "apple", 200, 5.0),
            Product("p3", "apple", 300, 3.0),
        ]
        
        result = processor.process(products)
        
        assert len(result.data) == 1
        assert result.data[0] == ("apple", 4.0)  # (4+5+3)/3 = 4.0
    
    def test_process_multiple_brands(self, processor):
        products = [
            Product("p1", "apple", 100, 4.0),
            Product("p2", "apple", 200, 5.0),
            Product("p3", "samsung", 300, 3.0),
            Product("p4", "samsung", 400, 4.0),
            Product("p5", "xiaomi", 500, 5.0),
        ]
        
        result = processor.process(products)
        
        assert len(result.data) == 3

        assert result.data[0] == ("xiaomi", 5.0)
        assert result.data[1] == ("apple", 4.5)  
        assert result.data[2] == ("samsung", 3.5)  
    
    def test_rating_rounding(self, processor):
        products = [
            Product("p1", "brand1", 100, 4.333),
            Product("p2", "brand1", 200, 4.666),
        ]
        
        result = processor.process(products)
        
        assert result.data[0] == ("brand1", 4.5)  