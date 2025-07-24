# Python 3.10 to be used
FROM python:3.10-slim

# Work folder to be created 
WORKDIR /app

# Requirements to be installed
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Port 5000 to be kept open for flask
EXPOSE 5000

# Run file when app starts
CMD ["python", "app.py"]
