FROM python:3.12-slim
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libblas-dev \
    liblapack-dev \
    libc-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir \
    https://files.pythonhosted.org/packages/ea/43/3f8069b168d5d7f8a7b702b5b688086bbed4c8534ec2e773c6cc0f39a2f3/blis-0.7.11-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]