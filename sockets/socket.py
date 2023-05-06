from fastapi import APIRouter,WebSocket,WebSocketDisconnect
print("Khởi tạo socket")
socket_router = APIRouter()
@socket_router.websocket_route("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"You said: {data}")
    except WebSocketDisconnect:
        await websocket.close()