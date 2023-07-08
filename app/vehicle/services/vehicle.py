from PIL import Image
import cv2
import math 
from os.path import isdir
import numpy as np
import base64
import os
from ultralytics import YOLO
IMAGE_USERS_PATH = "./public/images/users"
model_v8 = YOLO("D:/CAPSTONE2023/model/done_train.pt")
yolo_license_platev8 = YOLO("D:/CAPSTONE2023/model/best.pt")
# Update configuration
class VehicleServices:
    def __init__(self):
        self.listlb = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','K','L','M', 'N','P','S','T','U','V','X','Y','Z','0']
    def convertbase64 (self,string64 ):
        decoded_data = base64.b64decode(string64)
        np_data = np.fromstring(decoded_data, np.uint8)
        image = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
        
        return image
    def checkDetailVehicle(self, imagelp):
        # Convert String64 to Image 
        img = self.convertbase64(imagelp)
        
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        cv2.imwrite("D:/CAPSTONE2023/ImageTestTemp/testImage2.jpg",img)
        results = model_v8.predict(img)
        lableDetect =  results[0].names
        bounding_boxes =results[0].boxes.data
        bounding_boxes_value = bounding_boxes.to("cpu").tolist()
        list_read_plates = set()
        vehicle = ""
        max = 0
        for bbox in bounding_boxes_value:
            xmin, ymin, xmax, ymax,p,name = bbox
            print("detect",xmin, ymin, xmax, ymax,lableDetect[int(name)])
            if name == 0.0:
                crop_img = img[int(ymin):int(ymax), int(xmin):int(xmax)]
                cv2.imwrite("D:/CAPSTONE2023/ImageTestTemp/testImage.jpg",crop_img)
                lp = self.read_plate_v8(yolo_license_platev8, crop_img)
                if lp != "unknown":
                    print("lp",lp)
                    list_read_plates.add(lp)
            elif p > max:
                vehicle = name
        message= ""
        if vehicle == "":
            message = "Not Detected Vehicle"
        else:
            vehicle = lableDetect[int(vehicle)]
        if len(list_read_plates) == 0: # If Not detect characters, return vehicle = ""
            vehicle = ""
            list_read_plates.add(("",""))
            message = "Not Recognize Vehicle"
            
        first_element_lp = next(iter(list_read_plates))
        return vehicle,first_element_lp[0],first_element_lp[1], message
    def addVehicleUser(self, userid, vehicleImage,lp):
        img = self.convertbase64(vehicleImage)
        path_img_detected = IMAGE_USERS_PATH +str(userid) + " vehicle/"
        if isdir(path_img_detected) == False:     
            os.makedirs(path_img_detected)
        lpImage_path = path_img_detected + "/lp_{}.jpg".format(lp)
        cv2.imwrite(lpImage_path, img)
        return lpImage_path
    def linear_equation(self,x1, y1, x2, y2):
        b = y1 - (y2 - y1) * x1 / (x2 - x1)
        a = (y1 - b) / x1
        return a, b

    def check_point_linear(self,x, y, x1, y1, x2, y2):
        a, b = self.linear_equation(x1, y1, x2, y2)
        y_pred = a*x+b
        return(math.isclose(y_pred, y, abs_tol = 3))
    def read_plate_v8(self,yolo_license_platev8, im):
        LP_type = "1"
        results = yolo_license_platev8.predict(im)
        bb_list = results[0].boxes.data.to("cpu").tolist()
        listlbModel = results[0].names
        if len(bb_list) == 0 or len(bb_list) < 7 or len(bb_list) > 10:
            return "unknown"
        center_list = []
        y_mean = 0
        y_sum = 0
        for bb in bb_list:
            x_c = (bb[0]+bb[2])/2
            y_c = (bb[1]+bb[3])/2
            y_sum += y_c
            center_list.append([x_c,y_c,bb[-1]])

        # find 2 point to draw line
        l_point = center_list[0]
        r_point = center_list[0]
        for cp in center_list:
            if cp[0] < l_point[0]:
                l_point = cp
            if cp[0] > r_point[0]:
                r_point = cp
        for ct in center_list:
            if l_point[0] != r_point[0]:
                if (self.check_point_linear(ct[0], ct[1], l_point[0], l_point[1], r_point[0], r_point[1]) == False):
                    LP_type = "2"

        y_mean = int(int(y_sum) / len(bb_list))
        #size = results.pandas().s

        # 1 line plates and 2 line plates
        line_1 = []
        line_2 = []
        license_plate = ""
        if LP_type == "2":
            for c in center_list:
                if int(c[1]) > y_mean:
                    line_2.append(c)
                else:
                    line_1.append(c)
            for l1 in sorted(line_1, key = lambda x: x[0]):
                license_plate += str(self.listlb[int(listlbModel[int(l1[2])])])
            license_plate += "-"
            for l2 in sorted(line_2, key = lambda x: x[0]):
                license_plate += str(self.listlb[int(listlbModel[int(l2[2])])])
        else:
            for l in sorted(center_list, key = lambda x: x[0]):
                license_plate += str(self.listlb[int(listlbModel[int(l[2])])])
        return license_plate,LP_type