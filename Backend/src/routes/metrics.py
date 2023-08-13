from fastapi import APIRouter, status, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from Backend.src.analytics_manager.user_engagement import user_activities, products_popularity, event_frequencies
from Backend.src.routes.connected_sessions_manager import ConnectionManager

router = APIRouter(prefix="/metrics")

available_metrics = [
    "user_activities",
    "products_popularity",
    "event_frequencies"
]


class MetricModel(BaseModel):
    name: str
    params: dict = None


@router.get("")
def get_available_metrics():
    return available_metrics


@router.post("")
def get_metric(model: MetricModel):
    if model.name not in available_metrics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    match model.name:
        case "user_activities":
            if "user_id" not in model.params:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

            return user_activities(model.params["user_id"])
        case "products_popularity":
            if "top_k" not in model.params:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

            return products_popularity(model.params["top_k"])
        case "event_frequencies":
            return event_frequencies()


@router.websocket("/ws")
async def activity_change(websocket: WebSocket):
    manager = ConnectionManager()
    await manager.connect(websocket)
    try:
        while True:
            event = await websocket.receive_json()
            await manager.broadcast(event)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

