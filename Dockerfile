# Resume AI Analyzer - Docker Deployment
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements-deploy.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements-deploy.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Install spaCy and download model
RUN pip install spacy
RUN python -m spacy download en_core_web_sm

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p Uploaded_Resumes

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "App_fixed.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
