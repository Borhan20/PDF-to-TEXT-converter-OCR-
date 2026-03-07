FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    tesseract-ocr-fra \
    tesseract-ocr-deu \
    libtesseract-dev \
    poppler-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy project configuration
COPY pyproject.toml poetry.lock* ./

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy project source
COPY . .

# Install the project itself
RUN poetry install --no-interaction --no-ansi

# Expose Streamlit port
EXPOSE 8501

# Entry point
ENTRYPOINT ["streamlit", "run", "src/ocr_pdf_converter/app.py"]
