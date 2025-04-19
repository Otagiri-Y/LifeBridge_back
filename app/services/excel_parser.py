# app/services/excel_parser.py

from typing import Dict
import pandas as pd
from fastapi import UploadFile
from io import BytesIO

# 分類名の正規化（項目の揺れを防ぐ）
STANDARD_SECTION_KEYS = {
    "沿革": "history",
    "取引経緯": "deal_history",
    "経営理念": "philosophy",
    "経営ビジョン": "philosophy",
    "経営方針": "philosophy",
    "モットー": "philosophy",
    "経営基盤": "foundation",
    "業界環境": "foundation",
    "特色": "foundation",
    "強み": "strength",
    "弱み": "strength",
    "他社競合": "strength",
    "特記事項": "other",
    "その他": "other"
}

def normalize_section_key(raw_key: str) -> str:
    for keyword, standard_key in STANDARD_SECTION_KEYS.items():
        if keyword in raw_key:
            return standard_key
    return "unknown"

def parse_excel_sections(file: UploadFile) -> Dict[str, str]:
    contents = file.file.read()
    df = pd.read_excel(BytesIO(contents), header=None)

    result = {}
    for row in df.itertuples(index=False):
        if len(row) >= 2:
            raw_key, content = row[0], row[1]
            if pd.notna(raw_key) and pd.notna(content):
                section_key = normalize_section_key(str(raw_key))
                result[section_key] = str(content)

    return result
