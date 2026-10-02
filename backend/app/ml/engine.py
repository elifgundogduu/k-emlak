from backend.app.core.locations import ISTANBUL_LOCATIONS, NEIGHBORHOOD_PREMIUMS

class ValuationModel:
    def __init__(self):
        self.district_base_sqm_prices = {
            "Beşiktaş": 135000, "Sarıyer": 120000, "Kadıköy": 115000, "Adalar": 95000,
            "Bakırköy": 90000, "Şişli": 85000, "Beyoğlu": 80000, "Üsküdar": 80000,
            "Ataşehir": 70000, "Beykoz": 65000, "Zeytinburnu": 65000, "Kağıthane": 60000,
            "Maltepe": 60000, "Fatih": 55000, "Eyüpsultan": 55000, "Kartal": 52000,
            "Ümraniye": 50000, "Küçükçekmece": 50000, "Bahçelievler": 48000, "Başakşehir": 48000,
            "Çekmeköy": 46000, "Beylikdüzü": 42000, "Güngören": 42000, "Bayrampaşa": 42000,
            "Pendik": 42000, "Gaziosmanpaşa": 40000, "Tuzla": 40000, "Sancaktepe": 38000,
            "Şile": 38000, "Bağcılar": 38000, "Avcılar": 36000, "Büyükçekmece": 36000,
            "Esenler": 35000, "Sultangazi": 33000, "Silivri": 30000, "Sultanbeyli": 30000,
            "Esenyurt": 28000, "Çatalca": 28000, "Arnavutköy": 27000
        }
        self.default_sqm_price = 45000

        self.room_multipliers = {
            "1+0 (Stüdyo)": 0.88,
            "1+1": 0.95,
            "2+1": 1.00,
            "3+1": 1.08,
            "3+2 (Dubleks)": 1.15,
            "4+1": 1.16,
            "4+2 (Dubleks)": 1.22,
            "5+1": 1.25,
            "5+2 (Çatı Dubleksi)": 1.32,
            "6+1 ve Üzeri": 1.35,
            "6+2 (Müstakil / Villa Dubleks)": 1.45
        }

        self.floor_multipliers = {
            "Bodrum Kat": 0.82,
            "Bahçe / Giriş Katı": 0.92,
            "Yüksek Giriş": 0.96,
            "1. Kat": 1.02,
            "2. Kat": 1.04,
            "3. Kat": 1.05,
            "4. Kat": 1.05,
            "5. Kat": 1.05,
            "Ara Kat (6-10)": 1.08,
            "Üst Kat (10+)": 1.12,
            "Çatı Dubleksi": 1.18,
            "Bahçe Dubleksi": 1.12,
            "Müstakil / Villa": 1.30
        }

    def predict(self, district: str, neighborhood: str = "Merkez", listing_type: str = "Satılık", is_furnished: bool = False, floor_type: str = "2. Kat", gross_sqm: float = 100.0, room_count: str = "2+1", building_age: int = 5, user_price: float = None):
        try:
            gross_sqm = float(gross_sqm)
        except Exception:
            gross_sqm = 100.0

        try:
            building_age = int(building_age)
        except Exception:
            building_age = 5

        base_unit_price = self.district_base_sqm_prices.get(district, self.default_sqm_price)
        neighborhood_multiplier = NEIGHBORHOOD_PREMIUMS.get(neighborhood, 1.0)
        room_factor = self.room_multipliers.get(room_count, 1.0)
        floor_factor = self.floor_multipliers.get(floor_type, 1.0)
        age_depreciation = max(0.55, 1.0 - (building_age * 0.007))

        furnished_factor = (1.25 if listing_type == "Kiralık" else 1.06) if is_furnished else 1.0

        sale_price = gross_sqm * base_unit_price * neighborhood_multiplier * room_factor * floor_factor * age_depreciation * furnished_factor

        if listing_type == "Kiralık":
            estimated_price = round(sale_price / 220, -1)
        else:
            estimated_price = round(sale_price, 2)

        confidence = 94.0 if neighborhood in NEIGHBORHOOD_PREMIUMS else 89.0

        status_tag = "Normal"
        if user_price is not None:
            try:
                user_price = float(user_price)
                if user_price > 0:
                    diff_ratio = (user_price - estimated_price) / estimated_price
                    if diff_ratio < -0.10:
                        status_tag = "Uygun Fiyatlı"
                    elif diff_ratio > 0.10:
                        status_tag = "Pahalı"
                    else:
                        status_tag = "Normal"
            except Exception:
                pass

        return {
            "estimated_price": estimated_price,
            "listing_type": listing_type,
            "is_furnished": is_furnished,
            "status_tag": status_tag,
            "confidence_score": confidence
        }

valuation_engine = ValuationModel()
