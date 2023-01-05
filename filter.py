from abc import ABC, abstractmethod
import numpy as np
import os
gstreamer_dir = os.getenv('GSTREAMER_DIR') # None
gstreamerPath = gstreamer_dir+"\\bin"
os.add_dll_directory(gstreamerPath)
import cv2
import threading

class Param():
    def __init__(self) -> None:
        pass

class Params():
    def __init__(self) -> None:
        pass

class Filter(ABC):
    def __init__(self, name) -> None:
        self.name = name

    @abstractmethod
    def process(self, params, image):
        pass

    @abstractmethod
    def getUIMetadata(self):
        return []

    @abstractmethod
    def updateParams(self, params):
        pass

class VideoFilter():
    def __init__(self, size=None) -> None:
        self.video_url = ""
        self.filters = np.array([], dtype=Filter)
        self.size = size
        self.cap = None
        self.exporting = False
        self.mutex = threading.Lock()

    def stop(self):
        if self.cap is not None:
            self.cap.release()
            self.cap=None

    def selectVideo(self, url, streamer = cv2.CAP_GSTREAMER):
        if self.cap is not None:
            self.cap.release()

        self.video_url = url
        self.cap = cv2.VideoCapture(self.video_url) #IP Camera
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        return fps

    def addFilter(self, filter):
        self.mutex.acquire()
        self.filters = np.append(self.filters, filter)
        self.mutex.release()

    def getFilters(self):
        return self.filters

    def exportVideo(self, size, out_path_name):
        print("begin export")
        out = None
        cap = cv2.VideoCapture(self.video_url)
        fps = cap.get(cv2.CAP_PROP_FPS)
        if size is not None:
            out = cv2.VideoWriter(out_path_name, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

        if self.cap is not None:
            cap.set(cv2.CAP_PROP_FRAME_COUNT, 0)

        while(True):
            ret, frame = cap.read()
            if not ret:
                print("connection error")
                break
            
            if out is None:
                if self.size is None:
                    size = (frame.shape[1], frame.shape[0])
                
                else:
                    size = self.size

                out = cv2.VideoWriter(out_path_name, cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

            if size is not None:
                frame=cv2.resize(frame, size) 

            for i, f in enumerate(self.filters):
                frame = f.process(None, frame)

            out.write(frame)

        if out is not None:
            out.release()

        cap.release()
        print("end export")

    def nextFrame(self):
        if self.cap is None:
            return None

        if self.exporting:
            return None

        self.mutex.acquire()

        ret, frame = self.cap.read()
        if not ret:
            print("connection error")
            self.cap.release()
            self.cap = None
            self.mutex.release()
            return None

        if self.size is not None:
            frame=cv2.resize(frame, self.size) 

        for i, f in enumerate(self.filters):
            frame = f.process(None, frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.mutex.release()
        return frame

    def previewVideo(self):
        if self.cap is None:
            return

        self.mutex.acquire()

        while(True):
            ret, frame = self.cap.read()
            if not ret:
                print("connection error")
                break

            for i, f in enumerate(self.filters):
                frame = f.process(None, frame)

            frame=cv2.resize(frame, (960, 540)) 
            cv2.imshow('Capturing',frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break
            
            count = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
            print(count)

        self.cap.release()
        cv2.destroyAllWindows()
        self.mutex.release()