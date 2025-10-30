import pytest
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from csv_processor.validators import Validator
from csv_processor.exceptions import FileValidationError, ReportNotFoundError


class TestValidator:
    
    def test_validate_files_valid(self, tmp_path: Path):
        file1 = tmp_path / "test1.csv"
        file2 = tmp_path / "test2.csv"
        file1.write_text("test")
        file2.write_text("test")
        
        file_paths = [str(file1), str(file2)]
        result = Validator.validate_files(file_paths)
        
        assert len(result) == 2
        assert all(isinstance(p, Path) for p in result)
    
    @pytest.mark.parametrize("file_paths,expected_error", [
        ([], "No files provided"),
        (["nonexistent.csv"], "File does not exist"),
        (["."], "Path is not a file"),
    ])
    def test_validate_files_invalid(self, file_paths, expected_error, tmp_path: Path):
        with pytest.raises(FileValidationError) as exc_info:
            Validator.validate_files(file_paths)
        
        assert expected_error in str(exc_info.value)
    
    def test_validate_files_wrong_extension(self, tmp_path: Path):
        wrong_file = tmp_path / "test.txt"
        wrong_file.write_text("test")
        
        with pytest.raises(FileValidationError) as exc_info:
            Validator.validate_files([str(wrong_file)])
        
        assert "File is not CSV" in str(exc_info.value)
    
    def test_validate_report_type_valid(self):
        available_reports = ["report1", "report2", "average-rating"]
        
        result = Validator.validate_report_type("average-rating", available_reports)
        
        assert result == "average-rating"
    
    def test_validate_report_type_invalid(self):
        available_reports = ["report1", "report2"]
        
        with pytest.raises(ReportNotFoundError) as exc_info:
            Validator.validate_report_type("invalid-report", available_reports)
        
        assert "invalid-report" in str(exc_info.value)
        assert "report1, report2" in str(exc_info.value)