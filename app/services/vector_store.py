# app/services/vector_store.py

from typing import Dict, List
from sentence_transformers import SentenceTransformer
import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Qdrantクライアント初期化
qdrant = QdrantClient(
    url=QDRANT_HOST,
    api_key=QDRANT_API_KEY,
)  # Azure用に後で変更可

# 埋め込みモデルの初期化（軽量なall-MiniLM）
model = SentenceTransformer("all-MiniLM-L6-v2")

# 使用するコレクション名（共通化）
COLLECTION_NAME = "company_sections"

# 初回のみ：コレクション作成
try:
    qdrant.get_collection(COLLECTION_NAME)
except Exception:
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

# セクションデータ（6分類）をQdrantに登録
def register_company_vectors(company_id: int, section_data: Dict[str, str]):
    points: List[PointStruct] = []

    for i, (section_key, text) in enumerate(section_data.items()):
        if not text.strip():
            continue
        vector = model.encode(text).tolist()
        point_id = company_id * 10 + i  # 固定ルール（例：1社につき10刻み）
        points.append(
            PointStruct(
                id=point_id,
                vector=vector,
                payload={"company_id": company_id, "section": section_key}
            )
        )

    if points:
        qdrant.upsert(collection_name=COLLECTION_NAME, points=points)

def build_user_query_text(orientation, preferences) -> str:
    parts = []
    if orientation:
        parts.append(orientation.work_purpose or "")
        parts.append(orientation.ideal_role or "")
        parts.append(orientation.personal_values or "")
        parts.append(orientation.contribute or "")
    if preferences:
        parts.append(preferences.atmosphere or "")
        parts.append(preferences.age_group or "")
        parts.append(preferences.work_style or "")
    return " ".join([p for p in parts if p.strip()])

def search_similar_companies_from_qdrant(query_text: str, top_k: int = 5) -> list[int]:
    query_vector = model.encode(query_text).tolist()
    search_result = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
    )
    company_ids = list({hit.payload["company_id"] for hit in search_result})
    return company_ids

def search_similar_companies_from_qdrant_with_score(query_text: str, top_k: int = 5) -> List[dict]:
    query_vector = model.encode(query_text).tolist()
    search_result = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
        with_vectors=False
    )

    results = []
    seen = set()
    for hit in search_result:
        cid = hit.payload["company_id"]
        if cid not in seen:
            seen.add(cid)
            results.append({
                "company_id": cid,
                "score": hit.score
            })
    return results

