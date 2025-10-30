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
                raise FileValidationError(f'Path os not a file: {file_path}')
            
            if path.suffix.lower() != '.csv':
                raise FileValidationError(f'File is not CSV: {file_path}')
            
            paths.append(path)

        return paths