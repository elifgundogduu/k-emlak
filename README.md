# 🏡 K-EMLAK - Gayrimenkul İlan ve Değerleme Platformu

K-EMLAK, gayrimenkul ilanlarını listeleme, detaylı inceleme, yapay zeka destekli fiyat değerleme ve dinamik veri tarama imkanı sunan modern bir emlak otomasyon sistemidir.

---

## 🚀 Özellikler

* **🏠 İlan Listeleme & Filtreleme:** Kiralık ve satılık gayrimenkul ilanlarını detaylı filtrelerle arama ve inceleme.
* **🤖 Yapay Zeka Değerleme Motoru (ML Engine):** Gayrimenkulün konumuna, oda sayısına, metrekaresine ve bina yaşına göre tahmini piyasa değerini hesaplama.
* **🕷️ Otomatik Veri Tarayıcı (Web Scraper):** Güncel gayrimenkul verilerini otomatik olarak toplama ve sisteme aktarma.
* **⚙️ Yönetici (Admin) Paneli:** İlan ekleme, düzenleme ve sistem verilerini yönetme paneli.
* **🌱 Otomatik Veri Yükleyici (Seed Data):** Test ve geliştirme ortamı için hazır örnek veri seti yükleme desteği.

---

## 🛠️ Kullanılan Teknolojiler

* **Backend:** Python 3.14+, FastAPI, Uvicorn
* **Frontend:** HTML5, CSS3, JavaScript, Jinja2 Template Engine
* **Veritabanı & ORM:** SQLite, SQLAlchemy
* **Makine Öğrenmesi & Veri İşleme:** NumPy, Custom Estimation Engine

---

## 💻 Kurulum ve Çalıştırma

### 1. Projeyi Klonlayın
```bash
git clone https://github.com/elifgundogduu/k-emlak.git
cd k-emlak
```

### 2. Sanal Ortamı Oluşturun ve Aktifleştirin
```bash
python -m venv venv
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r backend/requirements.txt
```

### 4. Örnek Verileri Veritabanına Yükleyin
```bash
python seed_data.py
```

### 5. Uygulamayı Başlatın
```bash
python backend/main.py
```
Uygulama tarayıcınızda `http://127.0.0.1:8000` adresinde çalışmaya başlayacaktır.

---

## 📁 Proje Yapısı

```text
k-emlak/
├── backend/
│   ├── app/
│   │   ├── core/         # Veritabanı ve konum yapılandırmaları
│   │   ├── ml/           # Fiyat değerleme ve makine öğrenmesi motoru
│   │   ├── models/       # Veritabanı varlık modelleri (Entities)
│   │   └── scrapers/     # Veri tarayıcı betikleri
│   ├── main.py           # FastAPI uygulama giriş noktası
│   └── requirements.txt  # Python bağımlılıkları
├── frontend/
│   └── templates/        # HTML arayüz şablonları (index, detail, admin...)
├── K-EMLAK.docx          # Proje dokümantasyonu ve gereksinimleri
├── seed_data.py          # Örnek veri yükleyici betik
└── update_links.py       # Link güncelleme aracı
```

---

## 📄 Lisans
Bu proje eğitim ve geliştirme amaçlı hazırlanmıştır.
