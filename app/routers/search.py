from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.user_preferences import UserPreferences
from app.models.user_orientation import UserOrientation
from app.models.company import Company
from app.models.job import Job
from app.db.session import get_db
from app.auth.dependencies import get_current_user
from typing import List
from app.schemas.search import JobSchema

router = APIRouter()

# ---------------------------
# キーワードマッチング辞書
# ---------------------------
purpose_keywords = {
    "収入確保": ["労働力確保", "経営補佐"],
    "人と関わりたい": ["来客対応", "地域連携"],
    "社会貢献": ["地域貢献", "社会貢献", "課題対応"],
    "暇つぶし": ["スポットでの雇用", "単発作業"],
    "生涯現役": ["継続就業", "地域連携"]
}

role_keywords = {
    "顧客対応": ["受付", "来客対応"],
    "アドバイザー": ["講師", "ガイド"],
    "サポート": ["補助スタッフ"],
    "個別作業": ["個別作業"],
    "地域連携": ["地域連携"]
}

value_keywords = {
    "自由": ["挑戦", "創造性"],
    "礼儀": ["感謝", "信頼"],
    "成長": ["学び", "成長"],
    "貢献": ["地域と共に", "社会課題に挑む"],
    "秩序": ["ルール", "信頼"],
    "意見": ["提案", "意見を活かす"]
}

mind_keywords = {
    "堅実・成熟型": ["安定", "礼儀", "人の役に立ちたい"],
    "成長志向・拡大型": ["成長", "学び", "自由"],
    "安定・資産整理型": ["安定", "地域", "礼儀"],
    "チャレンジ・再構築型": ["挑戦", "自由", "創造性"],
    "再建型・資産整理型": ["サポート", "社会貢献", "地域"],
    "撤退型・守り重視型": ["安定", "礼儀", "秩序"],
    "積極資金運用型": ["意見", "提案", "自分の考え"]
}

# ---------------------------
# 辞書を使ったあいまいマッチング
# ---------------------------
def fuzzy_match(user_value: str, target_value: str, dictionary: dict) -> bool:
    if not user_value or not target_value:
        return False
    for key, synonyms in dictionary.items():
        if key in user_value:
            if any(s in target_value for s in synonyms):
                return True
    return False

# ---------------------------
# CFから企業マインド分類
# ---------------------------
def classify_company_mind(operating_cf, investing_cf, financing_cf):
    if operating_cf > 0 and investing_cf <= 0 and financing_cf <= 0:
        return "堅実・成熟型"
    elif operating_cf > 0 and investing_cf > 0 and financing_cf > 0:
        return "成長志向・拡大型"
    elif operating_cf > 0 and investing_cf <= 0 and financing_cf > 0:
        return "成長志向・拡大型"
    elif operating_cf < 0 and financing_cf > 0:
        return "チャレンジ・再構築型"
    elif operating_cf < 0 and investing_cf > 0:
        return "再建型・資産整理型"
    elif operating_cf <= 0 and investing_cf <= 0 and financing_cf <= 0:
        return "危機的状態・継続懸念型"
    elif operating_cf < 0 and investing_cf <= 0 and financing_cf >= 0:
        return "撤退型・守り重視型"
    elif operating_cf > 0 and investing_cf >= 0 and financing_cf >= 0:
        return "積極資金運用型"
    else:
        return "未分類"

# ---------------------------
# スコア計算
# ---------------------------
def evaluate_score(user, pref, orient, job, company, company_mind):
    score = 0

    if user.job_type == job.company_job_type:
        score += 2

    if pref:
        if pref.atmosphere == company.company_atmosphere:
            score += 1
        if pref.age_group == company.company_age:
            score += 1
        if pref.work_style == company.company_style:
            score += 1

    if orient:
        if orient.work_purpose == job.employment_purpose or fuzzy_match(orient.work_purpose, job.employment_purpose, purpose_keywords):
            score += 1
        if orient.ideal_role == job.expected_role or fuzzy_match(orient.ideal_role, job.expected_role, role_keywords):
            score += 1
        if orient.contribute == company.customer:
            score += 1
        if orient.personal_values in (company.corporate_philosophy or "") or fuzzy_match(orient.personal_values, company.corporate_philosophy or "", value_keywords):
            score += 1
        # 企業マインドとの相性
        if any(k in (orient.personal_values or "") for k in mind_keywords.get(company_mind, [])):
            score += 1

    return score

# ---------------------------
# エンドポイント実装
# ---------------------------
@router.get("/api/user/search", response_model=JobSchema)
def search_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.user_id == current_user.user_id).first()
    pref = db.query(UserPreferences).filter(UserPreferences.user_id == user.user_id).first()
    orient = db.query(UserOrientation).filter(UserOrientation.user_id == user.user_id).first()

    jobs = db.query(Job).all()
    job_scores = []

    for job in jobs:
        company = db.query(Company).filter(Company.company_id == job.company_id).first()
        if not company:
            continue
        mind = classify_company_mind(company.operating_cf, company.investing_cf, company.financing_cf)
        score = evaluate_score(user, pref, orient, job, company, mind)
        job_scores.append((score, job))

    if orient and orient.work_purpose == "収入確保":
        sorted_jobs = sorted(job_scores, key=lambda x: (-x[0], -x[1].salary if x[1].salary else 0, x[1].job_id))
    else:
        sorted_jobs = sorted(
            job_scores,
            key=lambda x: (
                -x[0],
                0 if orient and orient.work_purpose == x[1].employment_purpose else 1,
                x[1].job_id
            )
        )

    if not sorted_jobs:
        raise HTTPException(status_code=404, detail="求人が見つかりませんでした。")

    return sorted_jobs[0][1]
