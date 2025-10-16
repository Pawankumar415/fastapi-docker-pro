# -------- Stage 1: Build dependencies --------
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build tools (only in this stage)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

COPY requirements.txt .

# Install all packages into a temporary folder
RUN pip install --no-cache-dir --user -r requirements.txt


# -------- Stage 2: Final lightweight image --------
FROM python:3.12-slim

WORKDIR /app

# Copy only necessary files from builder stage
COPY --from=builder /root/.local /root/.local

# Make sure Python can find the installed packages
ENV PATH=/root/.local/bin:$PATH

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

