from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from .database import engine, Base
    from .routers import admin, auth_router, developer
    from .config import settings
except ImportError:
    from database import engine, Base
    from routers import admin, auth_router, developer
    from config import settings

app = FastAPI(
    title="Project Management System",
    description="Backend API for managing projects, developers, and tasks",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth_router.router)
app.include_router(admin.router)
app.include_router(developer.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "1.0.0"}
