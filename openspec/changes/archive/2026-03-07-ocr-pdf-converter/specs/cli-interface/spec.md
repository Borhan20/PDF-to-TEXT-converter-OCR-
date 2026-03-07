## ADDED Requirements

### Requirement: CLI File Processing
The system SHALL provide a command-line interface to process a single PDF file.

#### Scenario: Process single file
- **WHEN** the user runs `ocr-pdf convert input.pdf --output result.txt`
- **THEN** the system MUST process `input.pdf` and save the extracted text to `result.txt`

### Requirement: CLI Directory Processing
The system SHALL support batch processing of all PDF files within a directory.

#### Scenario: Batch process directory
- **WHEN** the user runs `ocr-pdf convert ./my_pdfs/ --output-dir ./results/`
- **THEN** the system MUST process every `.pdf` file in `./my_pdfs/` and create corresponding `.txt` files in `./results/`
