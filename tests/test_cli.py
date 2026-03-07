from typer.testing import CliRunner
from ocr_pdf_converter.cli import app

runner = CliRunner()

def test_convert_command_exists():
    result = runner.invoke(app, ["convert", "--help"])
    assert result.exit_code == 0
    assert "convert" in result.stdout.lower()
    assert "input_path" in result.stdout.lower()

def test_app_help():
    # If there's only one command, --help might show the command help
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "convert" in result.stdout.lower()
