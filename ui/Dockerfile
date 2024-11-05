FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Streamlit uygulamasını başlat
CMD ["streamlit", "run", "app.py", "--server.port=8507", "--server.address=0.0.0.0"]
