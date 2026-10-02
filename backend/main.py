from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.core.database import init_db, get_db
from backend.app.models.entities import Property, ValuationHistory
from backend.app.ml.engine import valuation_engine
from backend.app.core.locations import ISTANBUL_LOCATIONS

app = FastAPI(title="K-EMLAK Değerleme Sistemi")

init_db()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

ROOM_LIST = [
    "1+0 (Stüdyo)", "1+1", "2+1", "3+1", "3+2 (Dubleks)",
    "4+1", "4+2 (Dubleks)", "5+1", "5+2 (Çatı Dubleksi)", "6+1 ve Üzeri", "6+2 (Müstakil / Villa Dubleks)"
]

FLOOR_LIST = [
    "Bodrum Kat", "Bahçe / Giriş Katı", "Yüksek Giriş",
    "1. Kat", "2. Kat", "3. Kat", "4. Kat", "5. Kat",
    "Ara Kat (6-10)", "Üst Kat (10+)", "Çatı Dubleksi", "Bahçe Dubleksi", "Müstakil / Villa"
]

def get_common_data(db: Session, portal=None, listing_type=None, is_furnished=None, district=None, neighborhood=None, room_count=None, floor_type=None, max_price=None):
    query = db.query(Property)

    if portal and portal.strip() != "":
        query = query.filter(Property.portal == portal)
    if listing_type and listing_type.strip() != "":
        query = query.filter(Property.listing_type == listing_type)
    if is_furnished is not None and str(is_furnished).strip() != "":
        furnished_bool = True if str(is_furnished) in ["1", "True", "true"] else False
        query = query.filter(Property.is_furnished == furnished_bool)
    if district and district.strip() != "":
        query = query.filter(Property.district == district)
    if neighborhood and neighborhood.strip() != "":
        query = query.filter(Property.neighborhood == neighborhood)
    if room_count and room_count.strip() != "":
        query = query.filter(Property.room_count == room_count)
    if floor_type and floor_type.strip() != "":
        query = query.filter(Property.floor == floor_type)

    parsed_max_price = None
    if max_price is not None and str(max_price).strip() != "":
        try:
            parsed_max_price = float(max_price)
            query = query.filter(Property.price <= parsed_max_price)
        except ValueError:
            parsed_max_price = None

    properties = query.all()
    enriched_listings = []
    for p in properties:
        pred = valuation_engine.predict(
            district=p.district,
            neighborhood=p.neighborhood,
            listing_type=p.listing_type,
            is_furnished=bool(p.is_furnished),
            floor_type=p.floor or "2. Kat",
            gross_sqm=p.gross_sqm,
            room_count=p.room_count or "2+1",
            building_age=p.building_age or 5,
            user_price=p.price
        )
        enriched_listings.append({
            "id": p.id,
            "title": p.title,
            "portal": p.portal,
            "district": p.district,
            "neighborhood": p.neighborhood,
            "full_address": p.full_address,
            "listing_type": p.listing_type,
            "is_furnished": p.is_furnished,
            "image_url": p.image_url,
            "source_url": p.source_url,
            "maps_url": p.address_query,
            "room_count": p.room_count,
            "gross_sqm": p.gross_sqm,
            "building_age": p.building_age,
            "floor": p.floor,
            "heating_type": p.heating_type,
            "price": p.price,
            "analysis_tag": pred["status_tag"]
        })

    total_properties = db.query(Property).count()
    total_sale = db.query(Property).filter(Property.listing_type == "Satılık").count()
    total_rent = db.query(Property).filter(Property.listing_type == "Kiralık").count()
    total_valuations = db.query(ValuationHistory).count()

    stats = db.query(
        Property.district,
        func.avg(Property.price / Property.gross_sqm).label("avg_sqm")
    ).filter(Property.listing_type == "Satılık").group_by(Property.district).order_by(func.avg(Property.price / Property.gross_sqm).desc()).all()

    labels = [s.district for s in stats]
    values = [round(float(s.avg_sqm), 0) for s in stats]
    history = db.query(ValuationHistory).order_by(ValuationHistory.created_at.desc()).limit(10).all()

    return {
        "istanbul_locations": ISTANBUL_LOCATIONS,
        "all_districts": sorted(list(ISTANBUL_LOCATIONS.keys())),
        "room_list": ROOM_LIST,
        "floor_list": FLOOR_LIST,
        "listings": enriched_listings,
        "selected_portal": portal or "",
        "selected_type": listing_type or "",
        "selected_furnished": str(is_furnished) if is_furnished is not None else "",
        "selected_district": district or "",
        "selected_neighborhood": neighborhood or "",
        "selected_room": room_count or "",
        "selected_floor": floor_type or "",
        "max_price": parsed_max_price or "",
        "total_properties": total_properties,
        "total_sale": total_sale,
        "total_rent": total_rent,
        "total_valuations": total_valuations,
        "chart_labels": labels,
        "chart_values": values,
        "history": history
    }

@app.get("/", response_class=HTMLResponse)
@app.get("/valuation", response_class=HTMLResponse)
@app.get("/listings", response_class=HTMLResponse)
@app.get("/admin", response_class=HTMLResponse)
def index(
    request: Request,
    portal: str = None,
    listing_type: str = None,
    is_furnished: str = None,
    district: str = None,
    neighborhood: str = None,
    room_count: str = None,
    floor_type: str = None,
    max_price: str = None,
    db: Session = Depends(get_db)
):
    data = get_common_data(db, portal, listing_type, is_furnished, district, neighborhood, room_count, floor_type, max_price)
    data["result"] = None
    return templates.TemplateResponse(request=request, name="index.html", context=data)

@app.get("/property/{property_id}", response_class=HTMLResponse)
def property_detail(property_id: int, request: Request, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="İlan bulunamadı")

    valuation_res = valuation_engine.predict(
        district=prop.district,
        neighborhood=prop.neighborhood,
        listing_type=prop.listing_type,
        is_furnished=bool(prop.is_furnished),
        floor_type=prop.floor or "2. Kat",
        gross_sqm=prop.gross_sqm,
        room_count=prop.room_count or "2+1",
        building_age=prop.building_age or 5,
        user_price=prop.price
    )

    return templates.TemplateResponse(
        request=request,
        name="detail.html",
        context={"property": prop, "valuation": valuation_res}
    )

@app.post("/valuation", response_class=HTMLResponse)
def perform_valuation(
    request: Request,
    listing_type: str = Form("Satılık"),
    is_furnished: str = Form("0"),
    floor_type: str = Form("2. Kat"),
    district: str = Form(...),
    neighborhood: str = Form(None),
    gross_sqm: float = Form(...),
    room_count: str = Form(...),
    building_age: int = Form(...),
    user_price: str = Form(None),
    db: Session = Depends(get_db)
):
    if not neighborhood or neighborhood.strip() == "":
        neighborhood = ISTANBUL_LOCATIONS.get(district, ["Merkez"])[0]

    parsed_user_price = None
    if user_price and user_price.strip() != "":
        try:
            parsed_user_price = float(user_price)
        except ValueError:
            parsed_user_price = None

    furnished_bool = True if is_furnished == "1" else False
    pred = valuation_engine.predict(
        district=district,
        neighborhood=neighborhood,
        listing_type=listing_type,
        is_furnished=furnished_bool,
        floor_type=floor_type,
        gross_sqm=gross_sqm,
        room_count=room_count,
        building_age=building_age,
        user_price=parsed_user_price
    )

    history_record = ValuationHistory(
        city="İstanbul",
        district=f"{district} / {neighborhood} ({room_count} - {floor_type})",
        listing_type=listing_type,
        gross_sqm=gross_sqm,
        room_count=room_count,
        building_age=building_age,
        predicted_price=pred["estimated_price"],
        status_tag=pred["status_tag"],
        confidence_score=pred["confidence_score"]
    )
    db.add(history_record)
    db.commit()

    data = get_common_data(db)
    data["result"] = pred
    return templates.TemplateResponse(request=request, name="index.html", context=data)
