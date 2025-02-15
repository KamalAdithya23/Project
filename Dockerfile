# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn openai requests beautifulsoup4 duckdb sqlite3

# Expose the FastAPI port
EXPOSE 8000

# Command to run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
