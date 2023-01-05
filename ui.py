from abc import ABC, abstractmethod
from subprocess import call
import tkinter as tk
from tkinter import filedialog as fd
import os
import utils
import numpy as np
import time
import threading

class ControllerInterface(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def main(self):
        pass

    @abstractmethod
    def callbackSample(self):
        pass

    @abstractmethod
    def callbackSampleEvent(self, event):
        pass

    @abstractmethod
    def getUIMetadata(self): 
        return [[]]

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def getFileTypes(self):
        pass

    @abstractmethod
    def stopCurrent(self):
        pass

    @abstractmethod
    def selectFile(self, path = None):
        pass

    @abstractmethod
    def exportData(self, path = None):
        pass

class Component(ABC):
    def __init__(self, name) -> None:
        self.name = name
        pass
    
    def getDescriptor(self):
        return {
                "name" : self.name,
                "type" : type(self)
            }

    @abstractmethod
    def buildComponent(self):
        pass

    @abstractmethod
    def eventCallback(self, event):
        pass

class Slider(Component):
    def __init__(self, name, begin, end, steps, callback) -> None:
        super().__init__(name=name)
        self.begin = begin
        self.end = end
        self.interval = end-begin
        self.step = self.interval / steps
        self.steps = steps
        self.current_value = None
        self.callback = callback

    def getHomogeneousCenteredValue(self):
        value = self.current_value.get()
        offset = self.interval / 2.0
        value = value - self.begin
        value = value - offset
        ratio = value / offset
        return ratio

    def getHomogeneousValue(self):
        value = self.current_value.get()
        offset = self.interval
        value = value - self.begin
        ratio = value / offset
        return ratio

    def getDescriptor(self):
        out = super().getDescriptor()
        out.update({
            "begin": self.begin,
            "end": self.end,
            "interval": self.interval,
            "step": self.step,
            "steps": self.steps,
        
        })
        return out
    
    def buildComponent(self, master):
        self.current_value = tk.DoubleVar()
        s = tk.Scale(master, name=self.name, from_=self.begin, to=self.end,tickinterval=np.ceil(self.steps / 2), variable=self.current_value, orient=tk.HORIZONTAL)
        s.set(self.interval / 2.0)
        s.pack()
        return s, self.current_value

    def eventCallback(self, event):
        print(event.widget._name)
        print(self.current_value)
        self.callback(event.widget._name)

class UI(ControllerInterface, threading.Thread):
    def __init__(self, controller, task_frame_rate) -> None:
        super().__init__()
        self.controller = controller
        self.task_frame_rate = task_frame_rate
        self.window = tk.Tk()
        
        #self.window.after(self.task_frame_rate, self.run)  # reschedule event in task_frame_rate seconds

        self.running = True
        self.window.protocol("WM_DELETE_WINDOW", self.stopCurrent)
        threading.Thread.__init__(self)

    def stopCurrent(self):
        self.controller.stopCurrent()
        self.running = False

    def run(self):
        start_time = time.perf_counter()
        out = self.controller.run()
        end_time = time.perf_counter()
        total_time = self.task_frame_rate - (end_time - start_time)
        print(total_time)
        if total_time > 0:
            time.sleep(total_time / 1000)

        return out

    def main(self):
        self.start()
        self.window.mainloop()
        
    def callbackSample(self):
        print("callbackSample ")
        self.controller.callbackSample()
        pass

    def callbackSampleEvent(self, event):
        print("callbackSampleEvent ",  event)
        self.controller.callbackSampleEvent(event)
        pass

    def getUIMetadata(self): 
        return [[]]
    
    def getFileTypes(self):
        return self.controller.getFileTypes()

    def selectFile(self, path = None):
        filetypes = self.getFileTypes()
        f = fd.askopenfile(filetypes=filetypes, initialdir="#Specify the file path")
        if f is None:
            return None

        f.close()
        print(f)
        return self.controller.selectFile(f.name)
    
    def exportData(self, path = None):
        f = fd.asksaveasfile(mode='w')
        if f is None:
            return None

        f.close()
        os.remove(f.name)
        self.controller.exportData(f.name)

