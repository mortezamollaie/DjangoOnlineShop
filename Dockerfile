# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Use Iranian mirrors for faster download
RUN echo "deb https://mirror.arvancloud.ir/debian/ bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb https://mirror.arvancloud.ir/debian/ bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb https://mirror.arvancloud.ir/debian-security/ bookworm-security main contrib non-free" >> /etc/apt/sources.list

# Install system dependencies
RUN apt-get update --fix-missing \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Configure PyPI with multiple mirrors and longer timeout
RUN pip config set global.timeout 300 && \
    pip config set global.retries 10

# Install Python dependencies with fallback mirrors
COPY --chown=appuser:appuser requirements.txt /app/
RUN pip install --no-cache-dir --user -r requirements.txt \
    --index-url https://pypi.org/simple/ \
    --extra-index-url https://mirror.arvancloud.ir/pypi/simple/ \
    --extra-index-url https://pypi.python.org/simple/ \
    --trusted-host pypi.org \
    --trusted-host mirror.arvancloud.ir \
    --trusted-host pypi.python.org

# Add user's local bin to PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Copy project with correct ownership
COPY --chown=appuser:appuser . /app/

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]