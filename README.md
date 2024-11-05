# Hava Durumu Paneli 🌤️

Bu proje, kullanıcıların şehir, sıcaklık birimi ve tarih aralığı seçerek geçmiş ve gelecek tarih aralığındaki hava durumu tahminlerini görüntüleyebileceği bir web uygulamasıdır. Uygulama, FastAPI ve Streamlit kullanılarak geliştirilmiş olup Docker ile konteynerleştirilmiştir. Hava durumu verileri Open-Meteo API’den çekilip PostgreSQL veritabanında saklanmaktadır.

## Özellikler

- Şehir seçimi (örnek şehirler: İstanbul, New York, Paris, New Delhi)
- Sıcaklık birimi seçimi (Celsius veya Fahrenheit)
- Geçmiş ve gelecek tarih aralığına göre hava durumu tahminleri
- Maksimum ve minimum sıcaklıklar ile ilgili istatistiksel özet
- Hava durumu verilerinin grafiksel ve tablo formatında sunumu

## Kullanılan Teknolojiler

- **FastAPI** - Backend API için
- **Streamlit** - Kullanıcı arayüzü için
- **PostgreSQL** - Hava durumu verilerini saklamak için
- **Docker** - Tüm bileşenleri izole bir ortamda çalıştırmak için
- **Docker Compose** - Çoklu konteyner yapılarını yönetmek için

## Kurulum

### Gereksinimler

- [Docker](https://www.docker.com/get-started) ve [Docker Compose](https://docs.docker.com/compose/install/) yüklü olmalıdır.

### Adımlar

1. Bu projeyi klonlayın:
   ```bash
   git clone https://github.com/kullanici_adiniz/hava-durumu-paneli.git
   cd hava-durumu-paneli
2. Docker konteynerlerini başlatın:
   ```bash
   docker-compose up --build -d
3. Uygulama başlatıldığında:
- Streamlit Arayüzü: http://localhost:8503
- FastAPI (Backend): http://localhost:8001


### Kullanım
- **Ayarlar Paneli**: Sol panelden şehir, tarih aralığı ve sıcaklık birimini seçin.
- **Tahmini Göster**: Ayarlar yapıldıktan sonra "Tahmini Göster" butonuna basarak hava durumu tahminlerini görüntüleyin.
- **Hava Durumu Özeti**: Seçilen tarih aralığına göre sıcaklık özetlerini ve günlük sıcaklık değişim grafiğini inceleyin.

## Proje Yapısı

project-root/
├── backend/
│   ├── Dockerfile               # FastAPI uygulaması için Docker yapılandırma dosyası
│   ├── main.py                  # Hava durumu verilerini sağlayan FastAPI uygulama dosyası
│   └── requirements.txt         # Backend bağımlılıkları
├── ui/
│   ├── Dockerfile               # Streamlit uygulaması için Docker yapılandırma dosyası
│   ├── app.py                   # Kullanıcı arayüzü ana dosyası
│   └── requirements.txt         # UI bağımlılıkları
├── .env                         # Ortak yapılandırma ayarlarını içeren dosya
└── docker-compose.yml           # Tüm servisleri başlatmak için Docker Compose dosyası



.env dosyasını oluşturun ve yapılandırın:
