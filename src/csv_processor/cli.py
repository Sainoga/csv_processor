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

def main(args: Optional[List[str]] = None) -> int:

    parser = create_parser()
    
    try:
        parsed_args = parser.parse_args(args)
        
        file_paths = Validator.validate_files(parsed_args.files)
        report_type = Validator.validate_report_type(
            parsed_args.report, 
            list(PROCESSORS.keys())
        )
        
        reader = CSVReader()
        products = reader.read_files(file_paths)
        
        if not products:
            print("No valid products found in the provided files.")
            return 0
        
        processor = PROCESSORS[report_type]
        report_result = processor.process(products)
        
        display_report(report_result)
        
        return 0
        
    except CSVProcessorError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())