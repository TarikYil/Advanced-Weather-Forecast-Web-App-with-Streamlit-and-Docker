from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, String, Float, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import httpx
import os
from datetime import datetime

app = FastAPI()

# Veritabanı bağlantısı
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Hava durumu verileri için model tanımı
class WeatherData(Base):
    __tablename__ = "weather_data"
    id = Column(String, primary_key=True, index=True)
    city = Column(String, index=True)
    date = Column(Date)
    max_temp = Column(Float)
    min_temp = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Veritabanını oluştur
Base.metadata.create_all(bind=engine)

# Open-Meteo API'den hava durumu verilerini çekme fonksiyonu
async def fetch_weather(city: str):
    city_coordinates = {
        "New Delhi": {"lat": 28.6139, "lon": 77.2090},
        "Istanbul": {"lat": 41.0082, "lon": 28.9784},
        "New York": {"lat": 40.7128, "lon": -74.0060},
        "Paris": {"lat": 48.8566, "lon": 2.3522}
    }

    if city not in city_coordinates:
        raise HTTPException(status_code=404, detail="Şehir bulunamadı.")

    coordinates = city_coordinates[city]
    async with httpx.AsyncClient() as client:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coordinates['lat']}&longitude={coordinates['lon']}&daily=temperature_2m_max,temperature_2m_min&timezone=Europe/Istanbul"
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Hava durumu verisi alınamadı.")

# Hava durumu verilerini al ve veritabanına kaydet
@app.get("/weather")
async def get_weather(city: str):
    weather_data = await fetch_weather(city)
    session = SessionLocal()

    # API yanıtını işleyerek veritabanına kaydet
    for date, max_temp, min_temp in zip(weather_data["daily"]["time"], weather_data["daily"]["temperature_2m_max"], weather_data["daily"]["temperature_2m_min"]):
        weather_entry = WeatherData(
            id=f"{city}_{date}",
            city=city,
            date=date,
            max_temp=max_temp,
            min_temp=min_temp
        )
        session.merge(weather_entry)  # Aynı veriyi günceller veya yeni kaydeder
    session.commit()
    session.close()

    return {
        "city": city,
        "dates": weather_data["daily"]["time"],
        "temperature_max": weather_data["daily"]["temperature_2m_max"],
        "temperature_min": weather_data["daily"]["temperature_2m_min"]
    }
