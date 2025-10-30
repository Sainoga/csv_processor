from typing import List, Dict
from collections import defaultdict

from ..models import Product, ReportResult
from .base import BaseProcessor

class AverageRatingProcessor(BaseProcessor):

        @property
    def report_name(self) -> str:
        return "average-rating"
    
    def process(self, products: List[Product]) -> ReportResult:
        if not products:
            return ReportResult(
                title="Average Rating by Brand",
                headers=["Brand", "Average Rating"],
                data=[]
            )
        
        # Group products by brand and calculate average rating
        brand_ratings: Dict[str, List[float]] = defaultdict(list)
        
        for product in products:
            brand_ratings[product.brand].append(product.rating)
        
        brand_averages = []
        for brand, ratings in brand_ratings.items():
            average_rating = sum(ratings) / len(ratings)
            brand_averages.append((brand, round(average_rating, 2)))
        
        brand_averages.sort(key=lambda x: x[1], reverse=True)
        
        return ReportResult(
            title="Average Rating by Brand",
            headers=["Brand", "Average Rating"],
            data=brand_averages
        )