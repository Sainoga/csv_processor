import pytest
from click.testing import CliRunner
from src.csv_processor.cli import main, create_parser


class TestCLI:
    
    @pytest.fixture
    def runner(self):
        return CliRunner()
    
    def test_parser_creation(self):
        parser = create_parser()
        
        assert parser is not None
        assert parser.description is not None
    
    def test_cli_help(self, runner):
        result = runner.invoke(main, ["--help"])
        
        assert result.exit_code == 0
        assert "Process CSV files" in result.output
        assert "--files" in result.output
        assert "--report" in result.output
    
    def test_cli_missing_arguments(self, runner):
        result = runner.invoke(main, [])
        
        assert result.exit_code != 0
        assert "error:" in result.output.lower()