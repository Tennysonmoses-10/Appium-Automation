FROM python:3.13-slim

LABEL maintainer="QA Automation Team <qa@partnerapp.com>"
LABEL description="Partner App QA Automation Framework"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV ENVIRONMENT=staging

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libappindicator1 \
    libasound2 \
    libatk1.0-0 \
    libcairo2 \
    libcups2 \
    libxss1 \
    libxtst6 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY pyproject.toml .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -e "."

# Copy project files
COPY . .

# Install Playwright browsers
RUN playwright install chromium firefox webkit

# Create necessary directories
RUN mkdir -p reports screenshots videos logs

# Set entrypoint
ENTRYPOINT ["python", "-m", "pytest"]

# Default command: run all tests with allure reporting
CMD ["tests/", "-v", "--alluredir=reports/allure", "-m", "smoke"]
