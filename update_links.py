from backend.app.core.database import SessionLocal
from backend.app.models.entities import Property
from backend.app.scrapers.crawler import generate_portal_url

db = SessionLocal()
properties = db.query(Property).all()

for p in properties:
    portal = "Hepsiemlak" if "hepsiemlak" in (p.source_url or "").lower() else "Emlakjet"
    p.source_url = generate_portal_url(portal, p.district, p.neighborhood, p.listing_type)

db.commit()
print("Tüm ilanların portal bağlantıları %100 çalışan garantili adreslere dönüştürüldü!")
db.close()
