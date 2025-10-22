from fastapi import APIRouter
from api.routes import routes_rag

router = APIRouter()
router.include_router(routes_rag.router, tags=["rag"], prefix="/v1")