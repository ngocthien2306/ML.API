from fastapi import APIRouter,WebSocket,WebSocketDisconnect,status
import base64
import json
import cv2
import numpy as np
from fastapi.responses import JSONResponse

from sockets.services.socket import LP_detect
print("Khởi tạo socket")
socket_router = APIRouter()
@socket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
                print("websocket")
                # Nhận dữ liệu từ client
                data = await websocket.receive_text()
                
                # Parse dữ liệu nhận được thành đối tượng JSON
                json_data = json.loads(data)
                # Lấy dữ liệu ảnh từ trường "Image"
                img_str = base64.b64decode(json_data['Image'])
                # Chuyển đổi dữ liệu ảnh thành đối tượng numpy array
                image_np = cv2.imdecode(np.frombuffer(img_str, np.uint8), cv2.IMREAD_COLOR)
                
                print(image_np.shape)

                predictions =json_data['Predictions']
                if len(predictions) != 0: 
                    listChar = LP_detect(image_np)
                    print("Chuoi bien so", listChar)
                # Xử lý dữ liệu nhận được tại đây
                # Gửi phản hồi về cho client
                await websocket.send_text(listChar)
    except Exception as e:
        print('message' ,str(e))
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )