# app/routers/upload.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.excel_parser import parse_excel_sections
from app.services.vector_store import register_company_vectors

router = APIRouter()

@router.post("/api/company/upload_excel")
def upload_company_excel(
    company_id: int,
    file: UploadFile = File(...)
):
    """
    # デバッグ用にログ出力
    print("ファイルアップロード開始")

    section_data = parse_excel_sections(file)
    print("セクションデータ抽出成功:", section_data)

    register_company_vectors(company_id=company_id, section_data=section_data)
    print("Qdrant 登録成功")

    return {"status": "success", "message": "企業データをQdrantに登録しました。"}
    """
    try:
        # Excelから6分類テキストを抽出
        section_data = parse_excel_sections(file)

        # Qdrantにベクトル登録
        register_company_vectors(company_id=company_id, section_data=section_data)

        return {"status": "success", "message": "企業データをQdrantに登録しました。"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"アップロードエラー: {str(e)}")