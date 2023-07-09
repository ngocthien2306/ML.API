from fastapi import APIRouter,WebSocket,WebSocketDisconnect
import base64
import json
from sockets.services.socket import checkDetailVehicle

print("Khởi tạo socket")
websocket_connections = []
socket_router = APIRouter()
@socket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        print("Test")
        websocket_connections.append(websocket)
        print("Connections: ",websocket_connections[0].client.host )
        while True:
                print("websocket")
                try:
                    # Nhận dữ liệu từ client
                    data = await websocket.receive_text()
                except WebSocketDisconnect as e:
                    print("Client disconnected", str(e))
                    websocket_connections.remove(websocket)
                    break
                # Parse dữ liệu nhận được thành đối tượng JSON
                json_data = json.loads(data)
                # Lấy dữ liệu ảnh từ trường "Image"
                img_str = base64.b64decode(json_data['Image'])
                # Chuyển đổi dữ liệu ảnh thành đối tượng numpy array
                #image_np = cv2.imdecode(np.frombuffer(img_str, np.uint8), cv2.IMREAD_COLOR)


                predictions =json_data['Predictions']
                print(predictions)
                listChar = ('','','','')
                if len(predictions) != 0: 
                    listChar = checkDetailVehicle(img_str)
                    if len(listChar) == 0 or not listChar:
                        listChar = "None"
                    print("Chuoi bien so", listChar)
                # Xử lý dữ liệu nhận được tại đây
                # Gửi phản hồi về cho client
                data = {
                    'TypeVehicle': listChar[0],
                    'Plate': listChar[1],
                    'TypeLp': listChar[2],
                    'Mess': listChar[3]
                }
                json_data = json.dumps(data)
                await websocket.send_text(json_data)
                    
    except Exception as e:
        print('Client disconnected:' ,str(e))
        return websocket_connections.remove(websocket)
        #return await websocket.close()
