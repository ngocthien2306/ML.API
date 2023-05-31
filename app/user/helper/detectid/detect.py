from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import numpy as np
from app.user.helper.ocr.text_recognition import TextRecognition
class yoloDetect:
    def __init__(self):
        self.text_recognition_model = TextRecognition()
        self.model = YOLO('/data/thinhlv/hung/Capstone/cccd_detect_character/runs/detect/train39/weights/best.pt') 
    def detect_id(self, image) -> str:
        try:
            image = Image.fromarray(image)
            
            results = self.model(image, iou=0.1)
            x1, y1, x2, y2,acc,l = None, None, None, None, None, None
            for data in results[0].boxes.data:

                x1, y1, x2, y2,acc,l = data.to('cpu').tolist()
                if(l == 3.0): # check acc
                    break
            if(x1 == None or y1 == None or x2 == None or y2 == None or acc == None or l == None):
                            return "Not Found"
            image_croped = image
            print(x1, y1, x2, y2,acc,l)
            cropped_image = image_croped.crop((x1, y1, x2, y2))
            cv2_image = cv2.cvtColor(np.array(cropped_image), cv2.COLOR_RGB2BGR)
            id = self.text_recognition_model.predict(cv2_image)
            return id
        except Exception as e:
            print(e)
            return str(e)
    