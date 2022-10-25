from abc import ABC, abstractmethod
import numpy as np
import cv2
class Param():
    def __init__(self) -> None:
        pass

class Params():
    def __init__(self) -> None:
        pass

class Filter(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def process(self, params, image):
        pass

    @abstractmethod
    def getUiMetadata(self):
        pass


class VideoFilter():
    def __init__(self) -> None:
        self.video_url = ""
        self.filters = np.array([], dtype=Filter)
        print("filters shape ", self.filters.shape)

        self.cap = None

    def selectVideo(self, url):
        self.cap = cv2.VideoCapture(url) #IP Camera


    def addFilter(self, filter):
        self.filters = np.append(self.filters, filter)
        print("filters shape ", self.filters.shape)

    def getFilters(self):
        pass

    def exportVideo(self):
        pass

    def previewVideo(self):
        if self.cap is None:
            return

        while(True):
            ret, frame = self.cap.read()
            if not ret:
                print("connection error")
                break

            for i, f in enumerate(self.filters):
                frame = f.process(None, frame)
                
            print("showing")
            print(frame.shape)
            frame=cv2.resize(frame, (960, 540)) 
            cv2.imshow('Capturing',frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'): #click q to stop capturing
                break
            
            #time.sleep(0.1)
            #count += 10
            count = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
            print(count)
            #cap.set(cv2.CAP_PROP_POS_FRAMES, count + 1)

        self.cap.release()
        cv2.destroyAllWindows()