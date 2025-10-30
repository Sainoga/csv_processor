import argparse
import sys
from typing import List, Optional

from tabulate import tabulate

from .models import CSVReader
from .validators import Validator
from .processors import PROCESSORS
from .exceptions import CSVProcessorError

def create_parser() -> argparse.ArgumentParser:
    
    parser = argparse.ArgumentParser(
        description="Process CSV files with product ratings and generate reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --files data1.csv data2.csv --report average-rating
  %(prog)s -f products.csv -r average-rating
        """
    )