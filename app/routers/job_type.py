from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.schemas.job_type import JobTypeUpdate

router = APIRouter()

@router.post("/api/user/job_type")
def update_job_type(
    job_data: JobTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.job_type = job_data.job_type
    db.commit()
    return {"message": "職種を更新しました"}
