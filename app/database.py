from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

from app.base import Base    # Import Base depuis base.py
from app.models import Scan  # Import Scan, OK car Base vient d'ailleurs

DATABASE_URL = "sqlite+aiosqlite:///./scans.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def save_scan(url: str, results: dict):
    async with async_session() as session:
        async with session.begin():
            scan = Scan(url=url, results=results)
            session.add(scan)
        await session.commit()
    return scan.id

async def get_scan(scan_id: int):
    async with async_session() as session:
        result = await session.execute(select(Scan).filter_by(id=scan_id))
        scan = result.scalar_one_or_none()
        return scan