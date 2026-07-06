"""
PAIOS Database Initialization Script
Run: python scripts/init_db.py
"""
from sqlalchemy import create_engine, Column, String, Text, DateTime, Float, JSON
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import settings

Base = declarative_base()

class AgentSnapshot(Base):
    __tablename__ = "agent_snapshots"
    id = Column(String, primary_key=True)
    agent_name = Column(String, nullable=False)
    summary = Column(Text)
    raw_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.now)

class MarketSnapshot(Base):
    __tablename__ = "market_snapshots"
    id = Column(String, primary_key=True)
    symbol = Column(String)
    price = Column(Float)
    change_pct = Column(Float)
    timestamp = Column(DateTime, default=datetime.now)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(String, primary_key=True)
    level = Column(String)  # critical/important/info
    message = Column(Text)
    agent_source = Column(String)
    timestamp = Column(DateTime, default=datetime.now)
    acknowledged = Column(String, default="false")

if __name__ == "__main__":
    print("Initializing PAIOS database...")
    try:
        engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(engine)
        print("✅ Database initialized successfully.")
    except Exception as e:
        print(f"⚠️  PostgreSQL not available ({e})")
        print("   PAIOS will run in memory-only mode.")
        print("   Install PostgreSQL or use SQLite by changing DATABASE_URL in .env:")
        print("   DATABASE_URL=sqlite:///paios.db")
