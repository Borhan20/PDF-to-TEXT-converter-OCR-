## ADDED Requirements

### Requirement: Language Selection Interface
The system SHALL provide a dropdown component to select the document language.

#### Scenario: Choose non-English language
- **WHEN** the user selects "Spanish" from the language dropdown and clicks "Run OCR"
- **THEN** the OCR engine processes the document using the corresponding language code (e.g., `spa`).

### Requirement: Language Persistence
The system SHALL remember the selected language across page navigations within the same session.

#### Scenario: Consistent language setting
- **WHEN** the user selects "French" and navigates to the next page
- **THEN** the language dropdown remains set to "French".
