import filter
import cv2
from ui import Slider
import numpy as np

class Brightness(filter.Filter):
    def __init__(self, name, begin, end, steps) -> None:
        super().__init__(name=name)
        self.slider = Slider(self.name, begin, end, steps, self.updateParams)

    def process(self, params, image):
        value = self.slider.getHomogeneousCenteredValue()
        value = np.exp(value)
        image = np.clip(image * value, 0 , 255).astype(np.uint8)
        return image #super().process(params, image)

    def getUIMetadata(self):
        meta = [
             self.slider
        ]
        return meta

    def updateParams(self, id):
        print("update ", id)
        print(self.slider.current_value.get())

class Hue(filter.Filter):
    def __init__(self, name) -> None:
        super().__init__(name=name)
        self.h = Slider("hue", 0,180,180, self.updateParams)
        self.s = Slider("saturation", 0,255,255, self.updateParams)
        self.v = Slider("value", 0,255,255, self.updateParams)

    def process(self, params, image):
        hue = self.h.getHomogeneousValue()
        sat = self.s.getHomogeneousValue()
        val = self.v.getHomogeneousValue()
        # convert to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        #h = hsv[:,:,0]
        #s = hsv[:,:,1]
        #v = hsv[:,:,2]
        h,s,v = cv2.split(hsv)
        # modify hue channel by adding difference and modulo 180
        diffh = int(np.round(hue * 180))
        diffs = int(np.round(sat * 255))
        diffv = int(np.round(val * 255))
        #hnew = (h + diffh)
        #snew = (s + diffs)
        #vnew = (v + diffv)
        hnew = np.clip(h + diffh, 0, 180)#.astype(np.uint8)
        snew = np.clip(s + diffs, 0, 255)#.astype(np.uint8)
        vnew = np.clip(v + diffv, 0, 255)#.astype(np.uint8)    
        #hnew = h + diffh
        #snew = s + diffs
        #vnew = v + diffv
        hsv_new = cv2.merge([hnew,snew,vnew])
        image = cv2.cvtColor(hsv_new, cv2.COLOR_HSV2BGR)
        return image # super().process(params, image)

    def getUIMetadata(self):
        meta = [
            self.h,
            self.s,
            self.v
            
        ]
        return meta
    
    def updateParams(self, id):
        print("update ", id)
        print(self.h.getHomogeneousCenteredValue())