from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..models import Admin, Developer
    from ..schemas import AdminRegister, LoginRequest, TokenResponse
    from ..auth import hash_password, verify_password, create_access_token
except ImportError:
    from database import get_db
    from models import Admin, Developer
    from schemas import AdminRegister, LoginRequest, TokenResponse
    from auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register-admin", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register_admin(body: AdminRegister, db: Session = Depends(get_db)):
    existing = db.query(Admin).filter(Admin.username == body.username).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")

    admin = Admin(username=body.username, password_hash=hash_password(body.password))
    db.add(admin)
    db.commit()
    db.refresh(admin)

    token = create_access_token({"sub": str(admin.id), "role": "admin"})
    return TokenResponse(access_token=token, role="admin")


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == body.username).first()
    if admin and verify_password(body.password, admin.password_hash):
        token = create_access_token({"sub": str(admin.id), "role": "admin"})
        return TokenResponse(access_token=token, role="admin")

    dev = db.query(Developer).filter(Developer.email == body.username).first()
    if dev and verify_password(body.password, dev.password_hash):
        token = create_access_token({"sub": str(dev.id), "role": "developer"})
        return TokenResponse(access_token=token, role="developer")

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
