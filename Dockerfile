# Gunakan Python base image
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Salin file aplikasi ke container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Set environment variable untuk Flask
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Jalankan aplikasi Flask
CMD ["python", "app.py"]