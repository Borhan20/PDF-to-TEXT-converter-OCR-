import typer
from typing import Optional
from typing_extensions import Annotated
from pathlib import Path
from rich.progress import Progress, track
from ocr_pdf_converter.pdf_processor import PDFProcessor
from ocr_pdf_converter.ocr_engine import OCREngine

app = typer.Typer(help="OCR PDF Converter - Convert PDF to Text")

@app.command(no_args_is_help=True)
def convert(
    input_path: Annotated[Path, typer.Argument(help="Path to PDF file or directory")],
    output: Annotated[Optional[Path], typer.Option("--output", "-o", help="Output text file (for single PDF)")] = None,
    output_dir: Annotated[Optional[Path], typer.Option("--output-dir", help="Output directory (for batch processing)")] = None,
    lang: Annotated[str, typer.Option("--lang", "-l", help="OCR language (e.g., 'eng', 'spa')")] = "eng",
    force: Annotated[bool, typer.Option("--force", "-f", help="Overwrite existing output files")] = False,
):
    """
    Convert a PDF file or a directory of PDF files to plain text.
    """
    if not input_path.exists():
        typer.echo(f"Error: {input_path} does not exist.")
        raise typer.Exit(code=1)

    if input_path.is_file():
        # Input validation: check for PDF extension
        if input_path.suffix.lower() != ".pdf":
            typer.echo(f"Error: {input_path} is not a PDF file.")
            raise typer.Exit(code=1)

        # Single file conversion
        if output is None:
            output = input_path.with_suffix(".txt")
        
        if output.exists() and not force:
            typer.echo(f"Error: Output file {output} already exists. Use --force to overwrite.")
            raise typer.Exit(code=1)

        typer.echo(f"Processing single file: {input_path}...")
        text = process_single_pdf(input_path, lang)
        
        output.write_text(text)
        typer.echo(f"Saved to {output}")

    elif input_path.is_dir():
        # Batch processing
        if output_dir is None:
            output_dir = input_path
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        pdf_files = list(input_path.glob("*.pdf"))
        if not pdf_files:
            typer.echo("No PDF files found in the directory.")
            return

        with Progress() as progress:
            task = progress.add_task("[green]Processing PDFs...", total=len(pdf_files))
            for pdf_file in pdf_files:
                progress.update(task, description=f"[cyan]Processing {pdf_file.name}")
                
                output_file = output_dir / pdf_file.with_suffix(".txt").name
                if output_file.exists() and not force:
                    typer.echo(f"Skipping {pdf_file.name}: {output_file} already exists.")
                    progress.advance(task)
                    continue

                text = process_single_pdf(pdf_file, lang)
                output_file.write_text(text)
                progress.advance(task)
        
        typer.echo(f"Batch processing complete. Results in {output_dir}")

def process_single_pdf(pdf_path: Path, lang: str) -> str:
    """Processes a single PDF and returns extracted text."""
    ocr_engine = OCREngine(default_lang=lang)
    
    with PDFProcessor(str(pdf_path)) as processor:
        # Try existing text layer
        text = processor.extract_text_layer()
        metadata = processor.get_metadata()
        page_count = metadata.get("page_count", 1)
        
        # Refined heuristic: if average characters per page is too low, try OCR
        # Threshold: < 20 characters per page on average OR total < 10 characters
        if len(text.strip()) < 10 or (len(text.strip()) / page_count) < 20:
            typer.echo("Searchable text layer is missing, empty, or insufficient. Running OCR...")
            images = processor.convert_to_images()
            ocr_results = []
            
            for img in track(images, description="[blue]Running OCR on pages"):
                ocr_results.append(ocr_engine.extract_text(img))
            text = "\n".join(ocr_results)
        else:
            typer.echo("Found searchable text layer. Direct extraction used.")
        
    return text

def main():
    app()

if __name__ == "__main__":
    main()
