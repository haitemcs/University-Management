from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.database import Base, engine, SessionLocal
from app.models import Role
from app.routers import auth, academic, reports

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        for name in ("admin", "teacher", "student"):
            if not db.query(Role).filter_by(name=name).first(): db.add(Role(name=name))
        db.commit()
    yield

app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(academic.router)
app.include_router(reports.router)

@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}
