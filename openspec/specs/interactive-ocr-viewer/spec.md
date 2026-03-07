# interactive-ocr-viewer Specification

## Purpose
TBD - created by archiving change streamlit-ocr-web-service. Update Purpose after archive.
## Requirements
### Requirement: Split-Pane Display
The system SHALL display the current PDF page image and its extracted text in a side-by-side columns layout.

#### Scenario: Visual layout
- **WHEN** a valid PDF is uploaded and a page is selected
- **THEN** the left column shows the page as a rendered image and the right column shows a text area with OCR results.

### Requirement: Page Navigation
The system SHALL provide controls to navigate through the pages of the uploaded PDF.

#### Scenario: Navigate to next page
- **WHEN** the user clicks the "Next Page" button on page 1 of a 2-page document
- **THEN** the viewer updates to show the content of page 2.

### Requirement: Text Editing and OCR Triggering
The system SHALL allow users to manually trigger OCR for the current page and edit the resulting text.

#### Scenario: Run OCR for single page
- **WHEN** the user clicks "Run OCR for this page"
- **THEN** the system processes only the current page and updates the corresponding text area.

