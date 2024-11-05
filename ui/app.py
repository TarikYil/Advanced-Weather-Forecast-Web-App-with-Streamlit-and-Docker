import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from datetime import datetime, timedelta

# .env dosyasını yükle
load_dotenv()

# FastAPI URL'ini .env dosyasından al
FASTAPI_PORT = os.getenv("FASTAPI_PORT", "8001")
FASTAPI_URL = f"http://fastapi-backend:{FASTAPI_PORT}"

# Tarayıcı sekme başlığı ve favicon ayarları
st.set_page_config(
    page_title="Hava Durumu Paneli",   # Sekme başlığı
    page_icon="🌤️",                    # Sekme ikonu olarak emoji kullanılıyor
    layout="wide"
)

# Ana başlık ve açıklama
st.title("🌤️ Hava Durumu Paneli")
st.markdown("Bu uygulama ile seçtiğiniz şehir için geçmiş ve gelecek tarih aralığındaki hava durumu tahminlerini grafik ve tablo şeklinde görüntüleyebilirsiniz.")

# Yan panel ayarları
with st.sidebar:
    st.header("⚙️ Ayarlar")
    city = st.selectbox("🌍 Şehir Seçin:", ["New Delhi", "Istanbul", "New York", "Paris"])
    unit = st.radio("🌡️ Sıcaklık Birimi:", ["Celsius", "Fahrenheit"], index=0)

    # Tarih aralığı seçimi için widget (geçmiş 7 gün ve gelecek 7 gün)
    st.write("📅 Tarih Aralığı Seçin:")
    date_selection = st.date_input(
        label="Tarih Aralığı",
        value=(datetime.today() - timedelta(days=7), datetime.today() + timedelta(days=7)),
        min_value=datetime.today() - timedelta(days=30),
        max_value=datetime.today() + timedelta(days=30)
    )

    # Renkli bir buton ile tahmini gösterme
    show_prediction = st.button("🔍 Tahmini Göster")

# Tarih aralığını ayarla
start_date = date_selection[0].strftime("%Y-%m-%d")
end_date = date_selection[1].strftime("%Y-%m-%d")

# Tahmini Göster Butonu ile işlem
if show_prediction:
    # FastAPI endpoint URL
    url = f"{FASTAPI_URL}/weather?city={city}&start_date={start_date}&end_date={end_date}"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()

        # Verileri DataFrame'e dönüştürme
        data = pd.DataFrame({
            "Tarih": pd.to_datetime(weather_data["dates"]),
            "Maks Sıcaklık": weather_data["temperature_max"],
            "Min Sıcaklık": weather_data["temperature_min"]
        })

        # Sıcaklık birimini dönüştürme
        if unit == "Fahrenheit":
            data["Maks Sıcaklık"] = data["Maks Sıcaklık"] * 9/5 + 32
            data["Min Sıcaklık"] = data["Min Sıcaklık"] * 9/5 + 32

        # Ortalama, maksimum ve minimum sıcaklıkları hesaplayın
        avg_max_temp = data["Maks Sıcaklık"].mean()
        avg_min_temp = data["Min Sıcaklık"].mean()
        highest_temp = data["Maks Sıcaklık"].max()
        lowest_temp = data["Min Sıcaklık"].min()

        # Gelişmiş İstatistik Gösterimi
        st.markdown("## 📊 Hava Durumu Özeti")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="🌡️ Ortalama Maksimum Sıcaklık", value=f"{avg_max_temp:.1f}° {unit}")
        col2.metric(label="🌡️ Ortalama Minimum Sıcaklık", value=f"{avg_min_temp:.1f}° {unit}")
        col3.metric(label="🔥 En Yüksek Sıcaklık", value=f"{highest_temp:.1f}° {unit}")
        col4.metric(label="❄️ En Düşük Sıcaklık", value=f"{lowest_temp:.1f}° {unit}")

        # Arayüzü iki sütunlu olarak düzenleme
        col1, col2 = st.columns([3, 1])

        with col1:
            # Grafik oluşturma
            st.markdown("## 📈 Sıcaklık Değişimi Grafiği")
            fig = px.line(data, x="Tarih", y=["Maks Sıcaklık", "Min Sıcaklık"],
                          labels={"value": f"Sıcaklık ({unit})", "variable": "Sıcaklık Türü"},
                          title=f"{city} için Maksimum ve Minimum Sıcaklık")
            fig.update_layout(legend_title_text="Sıcaklık Türü")
            st.plotly_chart(fig, use_container_width=True)

            # Veri tablosu gösterimi
            st.markdown("## 📅 Günlük Hava Durumu Verisi")
            st.dataframe(data.set_index("Tarih"))

        with col2:
            # Renkli bilgi kartları ve ek açıklamalar
            st.markdown("## ℹ️ Bilgilendirme")
            st.info(f"{city} için {start_date} ile {end_date} tarihleri arasındaki hava durumu özetlenmiştir. Yukarıdaki grafik ve tablo, sıcaklık değişimlerini günlük bazda göstermektedir.")
            st.write("**Not:** Veriler Open-Meteo API'den alınmaktadır. Güncellenen veriler farklı kaynaklardan gelen tahminlere göre değişebilir.")
            st.success("Bu tarih aralığında hava durumu verisi başarıyla yüklendi!")
    else:
        st.error("Hava durumu verisi alınamadı. Lütfen tekrar deneyin.")
else:
    st.markdown("### 🌟 Lütfen ayarlarınızı yapın ve tahmini görmek için 'Tahmini Göster' butonuna basın.")
