from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    portal = Column(String(50), default="Hepsiemlak", index=True)
    city = Column(String(50), default="İstanbul", index=True)
    district = Column(String(50), index=True)
    neighborhood = Column(String(50), index=True)
    full_address = Column(String(255))
    latitude = Column(Float, nullable=True) # Nokta atışı bina enlemi
    longitude = Column(Float, nullable=True) # Nokta atışı bina boylamı
    listing_type = Column(String(20), default="Satılık", index=True)
    image_url = Column(String(500), nullable=True)
    source_url = Column(String(500), nullable=True)
    address_query = Column(String(500), nullable=True)
    gross_sqm = Column(Float)
    room_count = Column(String(50))
    building_age = Column(Integer)
    floor = Column(String(50))
    heating_type = Column(String(50))
    is_furnished = Column(Boolean, default=False)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class ValuationHistory(Base):
    __tablename__ = "valuation_histories"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(50), default="İstanbul")
    district = Column(String(100))
    listing_type = Column(String(20), default="Satılık")
    gross_sqm = Column(Float)
    room_count = Column(String(50))
    building_age = Column(Integer)
    predicted_price = Column(Float)
    status_tag = Column(String(20))
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
