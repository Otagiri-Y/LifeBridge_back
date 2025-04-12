from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.user_preferences import UserPreferences
from app.models.user_orientation import UserOrientation
from app.auth.dependencies import get_current_user
from app.schemas.matching import UserMatchingUpdate

router = APIRouter()

@router.post("/api/user/matching")
def update_user_matching(
    matching_data: UserMatchingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ✅ preferences: なければ作る
    if current_user.preferences is None:
        current_user.preferences = UserPreferences(
            user_id=current_user.user_id
        )
        db.add(current_user.preferences)

    current_user.preferences.atmosphere = matching_data.atmosphere
    current_user.preferences.age_group = matching_data.age_group
    current_user.preferences.work_style = matching_data.work_style

    # ✅ orientation: なければ作る
    if current_user.orientation is None:
        current_user.orientation = UserOrientation(
            user_id=current_user.user_id
        )
        db.add(current_user.orientation)

    current_user.orientation.work_purpose = matching_data.work_purpose
    current_user.orientation.ideal_role = matching_data.ideal_role
    current_user.orientation.contribute = matching_data.contribute
    current_user.orientation.personal_values = matching_data.personal_values

    db.commit()

    return {"message": "ユーザーの希望条件・志向を更新しました"}
