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

    parser.add_argument(
        "--files", "-f",
        nargs="+",
        required=True,
        help="Paths to CSV files to process"
    )

    parser.add_argument(
        "--report", "-r",
        required=True,
        choices=list(PROCESSORS.keys()),
        help="Type of report to generate"
    )
    
    return parser

def display_report(report_result) -> None:
    """Display report result in console as table."""
    if not report_result.data:
        print("No data available for the report.")
        return
    
    print(f"\n{report_result.title}")
    print("=" * 50)
    print(tabulate(report_result.data, headers=report_result.headers, tablefmt="grid"))

