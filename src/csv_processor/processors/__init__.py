from .average_rating import AverageRatingProcessor

PROCESSORS = {
    AverageRatingProcessor().report_name: AverageRatingProcessor()
}

__all__ = ["PROCESSORS", "AverageRatingProcessor"]