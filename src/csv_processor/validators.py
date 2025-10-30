from pathlib import Path
from typing import List

from .exceptions import FileValidationError, ReportNotFoundError


class Validator:
    @staticmethod
    def validate_files(file_paths: List[str]) -> List[Path]:
        if not file_paths:
            raise FileValidationError('No files provided')
        
        paths = []
        for file_path in file_paths:
            path = Path(file_path)

            if not path.exists():
                raise FileValidationError(f'File does not exist: {file_path}')
            
            if not path.is_file():
                raise FileValidationError(f'Path is not a file: {file_path}')
            
            if path.suffix.lower() != '.csv':
                raise FileValidationError(f'File is not CSV: {file_path}')
            
            paths.append(path)

        return paths
    
    @staticmethod
    def validate_report_type(report_type: str, available_reports: List[str]) -> str:
        if report_type not in available_reports:
            raise ReportNotFoundError(
                f"Report type '{report_type}' not found. "
                f"Available reports: {', '.join(available_reports)}"
            )
        return report_type