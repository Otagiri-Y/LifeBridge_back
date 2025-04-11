from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.company import CompanyUpdate
from app.auth.dependencies import get_current_user  # ←ここをdependenciesからimport

router = APIRouter()

@router.post("/api/user/company")
def update_last_company(
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.last_company = company_data.company_name
    db.commit()
    return {"message": "所属会社名を更新しました"}
