# app/services/vector_store.py

from typing import Dict, List
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
import os

# 使用するコレクション名
COLLECTION_NAME = "company_sections"

# 遅延初期化（必要なときだけ実行）
def get_qdrant_client():
    return QdrantClient(
        url=os.getenv("QDRANT_HOST"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

def get_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def recreate_collection_if_needed():
    client = get_qdrant_client()
    try:
        client.get_collection(COLLECTION_NAME)
    except Exception:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

# セクションデータ（6分類）をQdrantに登録
def register_company_vectors(company_id: int, section_data: Dict[str, str]):
    recreate_collection_if_needed()

    model = get_model()
    client = get_qdrant_client()
    points: List[PointStruct] = []

    for i, (section_key, text) in enumerate(section_data.items()):
        if not text.strip():
            continue
        vector = model.encode(text).tolist()
        point_id = company_id * 10 + i
        points.append(
            PointStruct(
                id=point_id,
                vector=vector,
                payload={"company_id": company_id, "section": section_key}
            )
        )

    if points:
        client.upsert(collection_name=COLLECTION_NAME, points=points)

# ユーザーの入力を結合して検索用テキストを作成
def build_user_query_text(orientation, preferences) -> str:
    parts = []
    if orientation:
        parts.extend([
            orientation.work_purpose or "",
            orientation.ideal_role or "",
            orientation.personal_values or "",
            orientation.contribute or ""
        ])
    if preferences:
        parts.extend([
            preferences.atmosphere or "",
            preferences.age_group or "",
            preferences.work_style or ""
        ])
    return " ".join(p for p in parts if p.strip())

# 類似企業検索（IDのみ）
def search_similar_companies_from_qdrant(query_text: str, top_k: int = 5) -> list[int]:
    model = get_model()
    client = get_qdrant_client()
    query_vector = model.encode(query_text).tolist()

    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )
    return list({hit.payload["company_id"] for hit in search_result})

# 類似企業検索（スコア付き）
def search_similar_companies_from_qdrant_with_score(query_text: str, top_k: int = 5) -> List[dict]:
    model = get_model()
    client = get_qdrant_client()
    query_vector = model.encode(query_text).tolist()

    search_result = client.search(
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
            results.append({"company_id": cid, "score": hit.score})
    return results
