from fastapi import APIRouter, BackgroundTasks
from app.services.ingest_service import ingest_products

router = APIRouter()

@router.post("/ingest/products")
def ingest(background_tasks: BackgroundTasks):

    background_tasks.add_task(
        ingest_products,
        "app/data/products.json"
    )

    return {"status": "Ingestion started"}
